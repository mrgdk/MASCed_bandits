import numpy as np
import time
from random import sample
#from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits.Bandit import Bandit
import matplotlib.pyplot as plt



#formula = "ao"
FORMULA_FUNC = None

REWARD = 0
ACTION = 1




class DUCB(Bandit):
    def __init__(self, formula):
        """TODO: FIXED THE FORMULA PART WHERE PREVIOUSLY ELVIN WAS TRYING TO CONCATENATE THE FORMULA WITH 'SWUCB' ALTHOUGH IT'S AN INT."""
        super().__init__("DUCB-" + str(formula))

        self.discount = float(formula)
        self.bandit_round = -1
        self.game_list = []
        self.last_action = bandit_args["initial_configuration"]

        
    def start_strategy(self, reward):
        #print("loop")
        self.game_list.append([reward, self.last_action])

        self.bandit_round = self.bandit_round + 1

        if((self.bandit_round) < (len(self.arms))):
            #initial exploration    
            #print("INITIAL EXPLORE: START")  
            next_arm = self.arms[self.bandit_round]
            #print("INITIAL EXPLORE: CHOSE: " + str(next_arm))  

        else:
            scores = [str(self.reward_average(arm)) + " c: " + str(self.tuned(arm, sum([self.times_played(arm) for arm in self.arms]))) for arm in self.arms]
            #print("Scores were " + str(scores))
            next_arm = max(self.arms, key=lambda arm: \
                       self.reward_average(arm) + self.tuned(arm, sum([self.times_played(arm) for arm in self.arms])))
            #print("And I picked " + str(next_arm))

        self.last_action = next_arm
        return next_arm


    def reward_average(self, arm):
        #print("Considering arm: " + str(arm))
        r_sum = 0.0
        total_games = len(self.game_list)

        for i, game in enumerate(self.game_list):  
            if(game[ACTION] == arm): #the games in which arm was chosen
                #print("value added to sum: " + str(np.power(self.discount, total_games - i) * game[REWARD]))
                r_sum+=(np.power(self.discount, total_games - i) * game[REWARD])
     
        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played

    
    def sqreward_average(self, arm):
        r_sum = 0.0
        total_games = len(self.game_list)
        for i, game in enumerate(self.game_list):  
            if(game[ACTION] == arm): #the games in which arm was chosen
                r_sum+=np.square(np.power(self.discount, total_games - i) * game[REWARD])

        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played

    def times_played(self, arm):
        arm_played = 0.0
        total_games = len(self.game_list)
        for i, game in enumerate(self.game_list):
            if(game[ACTION] == arm): arm_played += np.power(self.discount, total_games - i) #Each time the g am


        return arm_played


    def tuned(self, arm, n):
        n_k = self.times_played(arm)
        #print("times arm played inside tuned " + str(n_k))
        #print("value of n inside tuned " + str(n))
        average_of_squares = self.sqreward_average(arm)
        square_of_average = np.square(self.reward_average(arm))
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        
        V_k = estimated_variance + np.sqrt(2 * param)
        
        #print("values inside tuned " + str((n_k,average_of_squares,square_of_average,estimated_variance,param,V_k)))
        confidence_value = np.sqrt(param * V_k)
        if(np.isnan(confidence_value)):
            #print("\n\n\n\ncaught a nan\n\n\n\n\n")
            return 0
        else:
            return confidence_value
    def visualize(self):
        if((self.bandit_round) < (len(self.arms))): return
        arm_names = []
        arm_rewards= []
        arm_conf = []
        [(arm_names.append(str(arm)), arm_rewards.append(self.reward_average(arm)), arm_conf.append(self.tuned(arm, sum([self.times_played(arm) for arm in self.arms])))) for arm in self.arms]
        reward_bar = plt.bar(arm_names, arm_rewards)
        confidence_bar = plt.bar(arm_names, arm_conf, bottom=arm_rewards)
        #plt.bar_label(reward_bar, padding=3)
        #plt.bar_label(confidence_bar, padding=3)
        plt.yticks(np.arange(1.0,3.00, step=0.05))
        plt.pause(0.05)
        plt.cla()
        plt.draw()