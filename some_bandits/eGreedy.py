
import numpy as np
import time
from utilities import calculate_utility, convert_conf
from bandit_options import bandit_args
from Bandit import Bandit

ACTION = 0
REWARD = 1
N_K = 2

DECAY_RATE = 1.6


def something(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
    print("thisworks")

class eGreedyC(Bandit):
    def __init__(self):
        #print("I have been created")
        self.arms = bandit_args["arms"]
        
        initial_configuration = bandit_args["initial_configuration"]

        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
        else:
            epsilon = 1.0
            action_reward_pairs = []
            for arm in self.arms:
                action_reward_pairs.append([arm, 0.0, 1.0]) 

            bandit_args["knowledge"] = (action_reward_pairs, self.arms.index(initial_configuration), epsilon)
            self.knowledge = bandit_args["knowledge"]
        

    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        
        #need an elegant way to handle the first read where knowledge doesn't exist yet
       
        action_reward_pairs = self.knowledge[0]
        last_action = self.knowledge[1]
        epsilon = self.knowledge[2]
        

        action_index = last_action
            
        current_action = action_reward_pairs[action_index]

        if(current_action[ACTION] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(current_action[ACTION]) + " is not reflected in SWIM's " + str((servers,dimmer)))


        results = []

        reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
        current_action[REWARD] = current_action[REWARD] + sum(reward)

        current_action[N_K] = current_action[N_K] + 1


        choice = np.random.random()

        if choice < epsilon: new_action = np.random.choice(len(self.arms))
        else: new_action = self.choose_action(action_reward_pairs)

        new_knowledge = (action_reward_pairs, new_action, epsilon/DECAY_RATE)

        bandit_args['knowledge'] = new_knowledge

        return convert_conf(action_reward_pairs[new_action][ACTION],current_action[ACTION])


    def choose_action(self, pairs):
        "Returns index in the pair list of the chosen action"

        highest = -99999999 # - sys.maxsize perhaps (python3 is unbounded)
        chosen_action = None

        for pair_index in range(len(pairs)):
            
            current_pair = pairs[pair_index]

            Q_a = current_pair[REWARD]/current_pair[N_K]

            if(Q_a > highest):
                highest = Q_a
                chosen_action = pair_index

        return chosen_action


    

    


