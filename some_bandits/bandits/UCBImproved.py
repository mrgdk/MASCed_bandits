import numpy as np
import time
from random import sample
from some_bandits.utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits.Bandit import Bandit



#formula = "ao"
FORMULA_FUNC = None

CUM_REWARD = 0
CUM_SQ_REWARD = 1
N_K = 2
trace_len = 15000 #the total time of chosen trace in SWIM in seconds
horizon = round(trace_len / 60) 




class UCBImproved(Bandit):
    def __init__(self, formula = None):
        super().__init__("UCB-Improved")
        
        self.removable_arms = [arm for arm in self.arms]
        self.arm_reward_pairs = {}
        for arm in self.arms: self.arm_reward_pairs[arm] = [0.0,0.0,0.0]
        self.last_action = bandit_args["initial_configuration"]
        self.delta_m = 1.0

        
        
    def start_strategy(self, reward):
   
        if(len(self.removable_arms) == 1): 
            print("converged")
            return self.removable_arms[0]
        
        self.arm_reward_pairs[self.last_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[self.last_action][CUM_SQ_REWARD]+=np.square(reward)
        self.arm_reward_pairs[self.last_action][N_K]+=1
        
        delta_sq = np.square(self.delta_m)

        n_m = np.ceil( (2 * np.log(horizon * delta_sq))/ delta_sq )

        for arm in self.removable_arms:
            if self.arm_reward_pairs[arm][N_K] < n_m: 
                print("Explore phase")
                self.last_action = arm
                return arm

        fac = np.sqrt(np.log(horizon * delta_sq) / (2 * n_m))
    
        pair_avgs = [self.arm_reward_pairs[arm][CUM_REWARD]/self.arm_reward_pairs[arm][N_K] \
                    for arm in self.removable_arms]

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