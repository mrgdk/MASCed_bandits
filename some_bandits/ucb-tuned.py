
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
SQUARES_SUM = 3

trace_len = 11340 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


initial_configuration = bandit_args["initial_configuration"]
class UCBTuned(Bandit):
    def __init__(self):
        self.formula = None
        self.arms = bandit_args['arms']
        self.knowledge = None
        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
        else:
            action_reward_pairs = [ [arm, 0.0, 0.0, 0.0] for arm in self.arms ]
            bandit_args["knowledge"] = (-1, action_reward_pairs, self.arms.index(initial_configuration))
            self.knowledge = bandit_args["knowledge"]
        
        
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        
        self.formula = self.formula_to_function(formula) #this shouldn't be done every time

        
   
        #need an elegant way to handle the first read where knowledge doesn't exist yet
      
        n_round = self.knowledge[0]
        action_reward_pairs = self.knowledge[1]
        last_action = self.knowledge[2]
        #knowledge = (round, action_reward_pairs)

        if((n_round + 1) < (len(self.arms))): #+1 because you are choosing the new action, which could be out of exploration range
            #initial exploration
            pair = action_reward_pairs[last_action]

            if(pair[ACTION] != (servers, dimmer)): 
                raise RuntimeError("Previously chosen configuration " + str(pair[ACTION]) + " is not reflected in SWIM's " + str((servers,dimmer)))

            reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
        
            pair[REWARD] = pair[REWARD] + sum(reward)
            pair[N_K] = pair[N_K] + 1
            pair[SQUARES_SUM] = pair[SQUARES_SUM] + np.square(reward)
        
            n_round = n_round + 1

            new_knowledge = (n_round,action_reward_pairs,n_round) #the round just also happens to be the index of action since we go through it one by one
            #save_to_pickle(new_knowledge, 'ucb_knowledge')
            bandit_args['knowledge'] = new_knowledge

            return convert_conf(action_reward_pairs[n_round][ACTION], pair[ACTION])
        else:
            #exploitation
    
            action_index = last_action

            current_action = action_reward_pairs[action_index]

            if(current_action[ACTION] != (servers, dimmer)): 
                raise RuntimeError("Previously chosen configuration " + str(current_action[ACTION]) + " is not reflected in SWIM's " + str((servers,dimmer)))


            results = []

            reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
            current_action[REWARD] = current_action[REWARD] + sum(reward)

            current_action[N_K] = current_action[N_K] + 1
            current_action[SQUARES_SUM] = current_action[SQUARES_SUM] + np.square(reward)

            total_count = sum([pair[N_K] for pair in action_reward_pairs])
            new_action = self.choose_action(action_reward_pairs,total_count)

            #don't really need to update the n_round anymore because we're out of initial exploration anyways
            new_knowledge = (n_round, action_reward_pairs, new_action)
            #save_to_pickle(new_knowledge, "ucb_knowledge")
            bandit_args['knowledge'] = new_knowledge

            return convert_conf(action_reward_pairs[new_action][ACTION],current_action[ACTION])


    def choose_action(self, pairs, n):
        "Returns index in the pair list of the chosen action"

        highest = -99999999 # - sys.maxsize perhaps (python3 is unbounded)
        chosen_action = None

        # print("len pair")
        # print(str(len(pairs)))
        #print("Picking arm now")
        for pair_index in range(len(pairs)):
            
            current_pair = pairs[pair_index]

            Q_a = current_pair[REWARD]/current_pair[N_K]
        

            confidence = self.calculate_confidence(current_pair, n)

            result = Q_a + confidence
            #print("Pair Index " + str(pair_index) + "has value " + str(result))
            if(result > highest): #and wf.criteria(current_pair[ACTION], wf)):
                #print("reached")
                highest = result
                chosen_action = pair_index

        # print("the value was " + str(highest))
        return chosen_action

    def calculate_confidence(self, pair, n):
        n_k = pair[N_K]
        squares_sum = pair[SQUARES_SUM]
        rewards_sum = pair[REWARD]

        average_of_squares = squares_sum / n_k
        square_of_average = np.square(rewards_sum / n_k)
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        V_j = estimated_variance + np.sqrt(2 * param)

        return np.sqrt(param * V_j)