
import numpy as np
import time
from random import sample
from some_bandits.utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits.Bandit import Bandit



REWARD = 0
ACTION = 1

trace_len = 11340 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


class UCBNorm(Bandit):
    def __init__(self, formula=None):
        super().__init__('ucb-normal')        
        self.bandit_round = 1
        self.last_action = bandit_args["initial_configuration"]
        self.game_list = []


                
    def start_strategy(self, reward):
         
        minimum_arm_plays = np.ceil(8 * np.log10(self.bandit_round))
        if minimum_arm_plays == 0: minimum_arm_plays = 0.1 #edge case for first round

        self.game_list.append([reward, self.last_action])
    
        self.bandit_round = self.bandit_round + 1

        next_arm = None
        for arm_i, arm in enumerate(self.arms):
            if(self.times_played(arm) < minimum_arm_plays):
                next_arm = arm
                break;         

        if(not next_arm): 
            
            for arm in self.arms:
                arm_avg = self.reward_average(arm)
                
            next_arm = next_arm = max(self.arms, key=lambda arm: \
                       self.reward_average(arm) + self.confidence_factor())

        self.last_action = next_arm
        return next_arm

    def reward_average(self, arm):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == arm): #the games in which arm was chosen
                r_sum+=game[REWARD]
     
        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played
    
    def times_played(self, arm):
        return len([game for game in self.game_list if game[ACTION] == arm])

    def score(self, arm):
        arm_avg = self.reward_average(arm)
        return arm_avg + self.confidence_factor(arm_avg, arm)

    def sqreward_average(self, arm):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == arm): #the games in which arm was chosen
                r_sum+=np.square(game[REWARD])

        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played


    def confidence_factor(self, emp_mean, arm):
        #sum of square rewards - avg rew
        n_k = times_played(arm)

        sqreward_sum = sqreward_average(arm) * n_k

        sq_means = (sqreward_sum - (np.square(emp_mean) * n_k)) / (n_k -1)

        log_factor = (np.log(self.bandit_round-1)) / n_k

        return np.sqrt(16 * sq_means * log_factor)

