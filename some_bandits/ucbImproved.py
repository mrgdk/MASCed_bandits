import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args
from Bandit import Bandit



#formula = "ao"
FORMULA_FUNC = None

REWARD = 0
ACTION = 1
trace_len = 108400 #the total time of chosen trace in SWIM in seconds
horizon = round(trace_len / 60) 



initial_configuration = bandit_args["initial_configuration"]
class ucbImprovedC(Bandit):
    def __init__(self):
        self.arms = bandit_args['arms']
        self.knowledge = None
        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
        else:
            removable_arms = [arm for arm in self.arms]
            bandit_args["knowledge"] = ([], self.arms.index(initial_configuration), 1.0, removable_arms)
            self.knowledge = bandit_args["knowledge"]
        
        
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        dimmer = round(dimmer,2)
        self.game_list, prev_action, delta_m, removable_arms = self.knowledge

        print(removable_arms)
        print((servers, dimmer))
        print("should equal ")
        print(self.arms[prev_action])
        if(self.arms[prev_action] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(self.arms[prev_action]) + " is not reflected in SWIM's " + str((servers,dimmer)))
        if(len(removable_arms) == 1): 
            print("converged")
            return convert_conf(removable_arms[0], self.arms[prev_action]) 
        
        reward, is_bound_diff, bound_delta = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
        if(is_bound_diff):
            for game in self.game_list: game[REWARD] = game[REWARD] * bound_delta
        print("rew is")
        print(reward)
        print("0")
        self.game_list.append((sum(reward), prev_action)) #this represents the return of the evaluator() in definition.py and may need to be adjusted.
 
        delta_sq = np.square(delta_m)

        n_m = np.ceil( (2 * np.log(horizon * delta_sq))/ delta_sq )

        print("nm is ")
        print(n_m)
        for arm in removable_arms:
            glob_index = self.arms.index(arm)
            if self.times_played(glob_index) < n_m: 
                print("Explore phase")
                bandit_args['knowledge'] = (self.game_list, glob_index, delta_m, removable_arms)
                return convert_conf(arm, self.arms[prev_action])

        fac = np.sqrt(  np.log(horizon * delta_sq) / (2 * n_m))
    
        pair_avgs = [self.reward_average(self.arms.index(arm)) for arm in removable_arms]

        del_boundary = max([pair_avg - fac for pair_avg in pair_avgs])

        del_candidates = []
        print("del boundary")
        print(del_boundary)
        for avg_i, arm_avg in enumerate(pair_avgs):

            print("less than boundary? ")
            print(arm_avg + fac)
            
            if (arm_avg + fac) < del_boundary:
                del_candidates.append(removable_arms[avg_i])
        print("to be removed")
        print(del_candidates)
        for candidate in del_candidates: removable_arms.remove(candidate) 

        bandit_args['knowledge'] = (self.game_list, prev_action, delta_m/2, removable_arms)
        self.knowledge = bandit_args['knowledge']

        return self.start_strategy(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula)
    
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