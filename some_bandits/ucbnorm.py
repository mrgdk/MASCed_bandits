
import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args
from Bandit import Bandit



ACTION = 0
REWARD = 1
SQ_REWARD = 2
N_K = 3

trace_len = 11340 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


initial_configuration = bandit_args["initial_configuration"]
class ucbnormC(Bandit):
    def __init__(self):
        self.arms = bandit_args['arms']
        self.knowledge = None
        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
        else:
            action_reward_pairs = [ [arm, 0.0, 0.0, 0.0] for arm in self.arms ] 
            bandit_args["knowledge"] = (1, action_reward_pairs, self.arms.index(initial_configuration))
            self.knowledge = bandit_args["knowledge"]
        
        
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        
       
        #need an elegant way to handle the first read where knowledge doesn't exist yet
      
        n_round = self.knowledge[0]
        action_reward_pairs = self.knowledge[1]
        last_action = self.knowledge[2]
    
        
        
        minimum_arm_plays = np.ceil(8 * np.log10(n_round))
        if minimum_arm_plays == 0: minimum_arm_plays = 0.1 #edge case for first round

        prev_pair = action_reward_pairs[last_action]

        if(prev_pair[ACTION] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(prev_pair[ACTION]) + " is not reflected in SWIM's " + str((servers,dimmer)))

        reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers, False)
        reward = sum(reward)
        prev_pair[REWARD] = prev_pair[REWARD] + reward
        prev_pair[SQ_REWARD] = prev_pair[SQ_REWARD] + np.square(reward)
        prev_pair[N_K] = prev_pair[N_K] + 1
    
        for p_i, pair in enumerate(action_reward_pairs):
            if(pair[N_K] < minimum_arm_plays):
                n_round = n_round + 1
                new_knowledge = (n_round,action_reward_pairs,p_i) 
                bandit_args['knowledge'] = new_knowledge
                return convert_conf(pair[ACTION], action_reward_pairs[last_action][ACTION])
            


        arm_chosen = self.choose_action(action_reward_pairs, n_round)
        n_round = n_round + 1
        new_knowledge = (n_round,action_reward_pairs, arm_chosen) 
        bandit_args['knowledge'] = new_knowledge

        return convert_conf(action_reward_pairs[arm_chosen][ACTION], prev_pair[ACTION])


    def choose_action(self, pairs, n):
        "Returns index in the pair list of the chosen action"

        highest = -99999999 #
        chosen_action = None

        for pair_index in range(len(pairs)):
            
            current_pair = pairs[pair_index]

            Q_a = current_pair[REWARD]/current_pair[N_K]
        

            confidence = self.confidence_factor(Q_a, current_pair, n)

            result = Q_a + confidence
            #print("Pair Index " + str(pair_index) + "has value " + str(result))
            if(result > highest): #and wf.criteria(current_pair[ACTION], wf)):
                #print("reached")
                highest = result
                chosen_action = pair_index

        # print("the value was " + str(highest))
        return chosen_action


    def confidence_factor(self, emp_mean, pair, n):
        
        sq_means = (pair[SQ_REWARD] - (pair[N_K] * np.square(emp_mean))) / (pair[N_K] - 1)

        log_factor = (np.log(n-1)) / pair[N_K]

        return np.sqrt(16 * sq_means * log_factor)

