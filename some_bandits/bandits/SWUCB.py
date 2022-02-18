import numpy as np
import time
from random import sample
from some_bandits.utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits.Bandit import Bandit



REWARD = 0
ACTION = 1
XI = 2


class SWUCB(Bandit):
    def __init__(self, formula):
        super().__init__("SWUCB-" + formula)
        #self.look_back = 65
        self.look_back = int(formula)

        self.bandit_round = -1
        self.game_list = []
        self.last_action = bandit_args["initial_configuration"]
        


    def start_strategy(self, reward):
               
        self.game_list.append([reward, self.last_action])

        self.bandit_round = self.bandit_round + 1

        if((self.bandit_round) < (len(self.arms))):
            #initial exploration      
            next_arm = self.arms[self.bandit_round]
        else:
            next_arm = max(self.arms, key=lambda arm: \
                       self.X_t(arm) + self.c_t(arm))

        self.last_action = next_arm
        return next_arm

    def N_t(self, arm):
        start_point = max(0, self.bandit_round-self.look_back+1)
        count = 0
        for game_index in range(start_point,self.bandit_round):
            if(self.game_list[game_index][ACTION] == arm):
                count += 1

        return count

    def X_t(self, arm):

        summated = 0

        start_point = max(0, self.bandit_round-self.look_back+1)
        for game_index in range(start_point,self.bandit_round):
            current_game = game_list[game_index]
            if(current_game[ACTION] == arm): #the games in which i was the arm
                X_s = current_game[REWARD]
                summated+=X_s
        try:
            times_arm_played = self.N_t(arm) 
            if(summated == 0 or times_arm_played == 0): return 0
            
            return summated/self.N_t(arm)
        except:
            print("Divide by zero error likely")
            print(self.game_list)
            print("Last tau games are")
            print(self.game_list[-self.look_back:])
            print("Length of game list is ")
            print(len(self.game_list))
            print("Result of N_t that was trigger is ")
            print(self.N_t(arm))
            print("and the arm causing it was ")
            print(arm)
            print("Value of summated is ")
            print(summated)
            exit(1)

        
    def c_t(self, arm):
        t_or_tau = min(self.bandit_round,self.look_back)
        res = self.tuned(arm, t_or_tau)

        return res
    
    def sqreward_average(self, arm):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == arm):
                r_sum+=np.square(game[REWARD])

        times_arm_played = self.N_t(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played
    
    def tuned(self, arm, n):
        n_k = self.N_t(arm)

        average_of_squares = self.sqreward_average(arm)
        square_of_average = np.square(self.X_t(arm))
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        V_k = estimated_variance + np.sqrt(2 * param)

        return np.sqrt(param * V_k)
        


