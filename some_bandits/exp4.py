import numpy as np
import time
from random import sample
from bandit_options import bandit_args
from utilities import convert_conf
from EXP3 import execute as exp3exec

ACTION = 0
REWARD = 1
N_K = 2

#ETA = 1


LIST_OF_GAMES = []



DISTR_FUNC = None
UPDATE_FUNC = None

trace_len = 6300 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
ETA = np.sqrt(np.log(len(arms)) / (len(arms) * total_count) )

initial_configuration = bandit_args["initial_configuration"]

def execute(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate):
    arms = bandit_args['arms']    
    
    algorithm = "exp4"

    knowledge = None
    #need an elegant way to handle the first read where knowledge doesn't exist yet
    if(bandit_args["knowledge"]):
        knowledge = bandit_args["knowledge"]
    else:
        action_reward_pairs = [ [arm, 0.0, 0.0] for arm in arms ] 
        #(arm, reward, count)
        #(action, reward, n_k)
        initial_PT = []
        initial_Sweights = [0] * len(arms)
        DISTR_FUNC(DISTR_FUNC(initial_PT, initial_Sweights))
        bandit_args["knowledge"] = (initial_Sweights, arms.index(initial_configuration), initial_PT)
        #(S_weights, last_conf, Pt)
        knowledge = bandit_args["knowledge"]
    

    #np.random.seed(seed)
    
    #Receive advice E^(t)
    # choose At from Pt where Pt = Qt of E^(t)
    # Estimate action rewards X^_ti = 1 - I{A_t=i} / P_ti + gamma (1 - X_t)
    # X^~_t = E^(t)X_t propogate rewards to the experts
    # Update dsitribution Q_t with exponential weighting

    S_weights = knowledge[0]
    current_action_i = knowledge[1]
    P_t = knowledge[2]

    ########
    reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
    result_sum = sum(reward)

    UPDATE_FUNC(S_weights, action_index, P_t, result_sum) #Update weights

    DISTR_FUNC(P_t, S_weights) #(re-)calculate Pt
    
    new_action = np.random.choice(np.arange(0, len(arms)), p= P_t) #sample action from Pt
    
    #wf.primary_data_provider["last_action"] = current_action[ACTION]

    #####
    #don't really need to update the n_round anymore because we're out of initial exploration anyways
    new_knowledge = (S_weights, new_action, P_t)
     #save_to_pickle(new_knowledge, "ucb_knowledge")
    bandit_args['knowledge'] = new_knowledge

    return convert_conf(arms[new_action],arms[current_action_i])

    
