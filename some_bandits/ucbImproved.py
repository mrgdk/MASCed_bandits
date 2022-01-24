import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args
from Bandit import Bandit



#formula = "ao"
FORMULA_FUNC = None

ACTION = 0
REWARD = 1
N_K = 2

trace_len = 11340 #the total time of chosen trace in SWIM in seconds
horizon = round(trace_len / 60) 



initial_configuration = bandit_args["initial_configuration"]
class ucbImprovedC(Bandit):
    def __init__(self):
        self.arms = bandit_args['arms']
        self.knowledge = None
        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
        else:
            action_reward_pairs = [ [arm, 0.0, 0.0] for arm in self.arms ] 
            bandit_args["knowledge"] = (action_reward_pairs, action_reward_pairs[self.arms.index(initial_configuration)], 1.0)
            self.knowledge = bandit_args["knowledge"]
        
        
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
          
        action_reward_pairs, prev_pair, delta_m = self.knowledge
        #print(action_reward_pairs)
        if(prev_pair[ACTION] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(prev_pair[ACTION]) + " is not reflected in SWIM's " + str((servers,dimmer)))

        if(len(action_reward_pairs) == 1): 
            #print("converged")
            return convert_conf(action_reward_pairs[0][ACTION], prev_pair[ACTION]) 
        
        reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)

        prev_pair[REWARD] = prev_pair[REWARD] + sum(reward)
        prev_pair[N_K] = prev_pair[N_K] + 1

        delta_sq = np.square(delta_m)

        n_m = np.ceil( (2 * np.log(horizon * delta_sq))/ delta_sq )

        for pair in action_reward_pairs:
            if pair[N_K] < n_m: 
                #print("Explore phase")
                bandit_args['knowledge'] = (action_reward_pairs, pair, delta_m)
                return convert_conf(pair[ACTION], prev_pair[ACTION])

        fac = np.sqrt(  np.log(horizon * delta_sq) / (2 * n_m))
    
        pair_avgs = [pair[REWARD] / pair[N_K] for pair in action_reward_pairs]

        del_boundary = max([pair_avg - fac for pair_avg in pair_avgs])

        del_candidates = []
        #print("del boundary")
        #print(del_boundary)
        for arm_i, pair in enumerate(action_reward_pairs):
            pair_avg = pair_avgs[arm_i]
            #print("less than boundary? ")
            #print(pair_avg + fac)
            
            if (pair_avg + fac) < del_boundary:
                del_candidates.append(pair)

        for candidate in del_candidates: action_reward_pairs.remove(candidate) 

        bandit_args['knowledge'] = (action_reward_pairs, prev_pair, delta_m/2)
        self.knowledge = bandit_args['knowledge']

        return self.start_strategy(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula)
