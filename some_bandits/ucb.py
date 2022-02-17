import numpy as np
import time
from random import sample
#from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from some_bandits.bandit_options import bandit_args
from some_bandits.Bandit import Bandit



#formula = "ao"
FORMULA_FUNC = None

REWARD = 0
ACTION = 1



trace_len = 15000 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


initial_configuration = bandit_args["initial_configuration"]
class ucbC(Bandit):
    def __init__(self, formula):
        self.name = "UCB-" + formula
        self.formula = self.formula_to_function(formula)
        self.arms = bandit_args['arms']
        self.knowledge = None

        self.bandit_round = -1
        self.game_list = []
        self.last_action = initial_configuration
        
    def start_strategy(self, reward):

        self.game_list.append([reward, self.last_action])

        self.bandit_round = self.bandit_round + 1

        if((self.bandit_round) < (len(self.arms))):
            #initial exploration      
            next_arm = self.arms[self.bandit_round]
        else:
            next_arm = max(self.arms, key=lambda arm: \
                       self.reward_average(arm) + self.formula(arm, self.bandit_round))

        self.last_action = next_arm
        return next_arm


    def formula_to_function(self, choice):
        funcs = {
                "FH": self.chapter7,
                "AO": self.asymptotically_optimal,
                "OG": self.auer2002UCB,
                "TN": self.tuned
            }
            
        func = funcs.get(choice)
        #print(func.__doc__)
        return func

    def reward_average(self, arm):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == arm): #the games in which arm was chosen
                r_sum+=game[REWARD]
     
        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played

    
    def sqreward_average(self, arm):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == arm): #the games in which arm was chosen
                r_sum+=np.square(game[REWARD])

        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played

    def times_played(self, arm):
        return len([game for game in self.game_list if game[ACTION] == arm])


    def chapter7(self, arm, n):
        global DELTA

        upper_term = 2 * np.log( (1 / DELTA) )
        
        to_be_sqrt = upper_term/self.times_played(arm)
        
        return np.sqrt(to_be_sqrt)

    def asymptotically_optimal(self, arm, t):
        T_i = self.times_played(arm)

        f_t = 1 + (t  * np.square(np.log(t)))

        upper_term = 2 * (np.log(f_t))

        lower_term =  T_i

        to_be_sqrt = upper_term/lower_term
        
        return np.sqrt(to_be_sqrt)

    def auer2002UCB(self, arm, t):
        T_i = self.times_played(arm)

        upper_term = 2 * (np.log(t))

        lower_term =  T_i

        to_be_sqrt = upper_term/lower_term
        
        return np.sqrt(to_be_sqrt)

    def tuned(self, arm, n):
        n_k = self.times_played(arm)

        average_of_squares = self.sqreward_average(arm)
        square_of_average = np.square(self.reward_average(arm))
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        V_k = estimated_variance + np.sqrt(2 * param)

        return np.sqrt(param * V_k)