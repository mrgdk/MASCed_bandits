
import numpy as np
import time
from random import sample
from some_bandits.utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits.Bandit import Bandit


CUM_REWARD = 0
CUM_SQ_REWARD = 1
N_K = 2

trace_len = 11340 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


class UCBNorm(Bandit):
    def __init__(self, formula=None):
        super().__init__('ucb-normal')        
        self.bandit_round = 1
        self.last_action = bandit_args["initial_configuration"]
        self.arm_reward_pairs = {}
        for arm in self.arms: self.arm_reward_pairs[arm] = [0.0,0.0,0.0]
        
                
    def start_strategy(self, reward):
         
        minimum_arm_plays = np.ceil(8 * np.log10(self.bandit_round))
        if minimum_arm_plays == 0: minimum_arm_plays = 0.1 #edge case for first round

        self.arm_reward_pairs[self.last_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[self.last_action][CUM_SQ_REWARD]+=np.square(reward)
        self.arm_reward_pairs[self.last_action][N_K]+=1
    
        self.bandit_round = self.bandit_round + 1

        next_arm = None
        for arm_i, arm in enumerate(self.arms):
            if(self.arm_reward_pairs[arm][N_K] < minimum_arm_plays):
                next_arm = arm
                break;         

        if(not next_arm): 
                            
            next_arm = next_arm = max(self.arms, key=lambda arm: \
                       self.reward_average(arm) + self.confidence_factor(arm))

        self.last_action = next_arm
        return next_arm

    def reward_average(self, arm):
        return self.arm_reward_pairs[arm][CUM_REWARD] / self.arm_reward_pairs[arm][N_K]  
    

    def confidence_factor(self, arm):
        #sum of square rewards - avg rew
        n_k = self.arm_reward_pairs[arm][N_K]  

        sqreward_sum = self.arm_reward_pairs[arm][CUM_SQ_REWARD]

        print((sqreward_sum, (np.square(self.arm_reward_pairs[arm][CUM_REWARD]) * n_k), n_k-1))
        sq_means = (sqreward_sum - (np.square(self.reward_average(arm)) * n_k)) / (n_k -1)

        log_factor = (np.log(self.bandit_round-1)) / n_k

        print((16,sq_means,log_factor))
        return np.sqrt(16 * sq_means * log_factor)

