import numpy as np
import time
from random import sample
from some_bandits.utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits.Bandit import Bandit



#formula = "ao"
FORMULA_FUNC = None

REWARD = 0
ACTION = 1
trace_len = 15000 #the total time of chosen trace in SWIM in seconds
horizon = round(trace_len / 60) 




class UCBImproved(Bandit):
    def __init__(self, formula = None):
        super().__init__("UCB-Improved")
        
        self.removable_arms = [arm for arm in self.arms]
        self.game_list = []
        self.last_action = bandit_args["initial_configuration"]
        self.delta_m = 1.0

        
        
    def start_strategy(self, reward):
   
        if(len(self.removable_arms) == 1): 
            print("converged")
            return self.removable_arms[0]
        
        self.game_list.append([reward, self.last_action]) #this represents the return of the evaluator() in definition.py and may need to be adjusted.
 
        delta_sq = np.square(self.delta_m)

        n_m = np.ceil( (2 * np.log(horizon * delta_sq))/ delta_sq )

        for arm in self.removable_arms:
            glob_index = self.arms.index(arm)
            if self.times_played(glob_index) < n_m: 
                print("Explore phase")
                self.last_action = arm
                return arm

        fac = np.sqrt(np.log(horizon * delta_sq) / (2 * n_m))
    
        pair_avgs = [self.reward_average(self.arms.index(arm)) for arm in self.removable_arms]

        del_boundary = max([pair_avg - fac for pair_avg in pair_avgs])

        del_candidates = []
        #print("del boundary")
        #print(del_boundary)
        for avg_i, arm_avg in enumerate(pair_avgs):

            #print("less than boundary? ")
            #print(arm_avg + fac)
            
            if (arm_avg + fac) < del_boundary:
                del_candidates.append(self.removable_arms[avg_i])
        #print("to be removed")
        #print(del_candidates)
        for candidate in del_candidates: self.removable_arms.remove(candidate) 

        self.delta_m = self.delta_m/2

        return self.start_strategy(reward)
    
    def times_played(self, i):
        return len([game for game in self.game_list if game[ACTION] == i])
    
    def reward_average(self, i):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == i): #the games in which i was the arm
                r_sum+=game[REWARD]
     
        times_i_played = self.times_played(i) 
        if(r_sum == 0 or times_i_played == 0): return 0
            
        return r_sum/times_i_played