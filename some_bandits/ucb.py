
import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args

def IEEESASO2019(pair, n):
    print("This is a form of UCB-tuned that may be incorrect")
    # "Function from the IEEE SASO 2019 paper by Porter and Rodrigues"
    # constant = 0.25

    # a_r_nk = pair
    # n_k = a_r_nk[N_K]

    # ln_n = np.log(n)

    # left_term = ln_n/n_k

    # right_term = constant * ((2.0 * ln_n) /n_k)
    
    # return np.sqrt(left_term * right_term)

def chapter7(pair, n):
    global DELTA

    upper_term = 2 * np.log( (1 / DELTA) )
    
    to_be_sqrt = upper_term/pair[N_K]
    
    return np.sqrt(to_be_sqrt)

def asymptotically_optimal(pair, t):
    
    T_i = pair[N_K]

    f_t = 1 + (t  * np.square(np.log(t)))

    upper_term = 2 * (np.log(f_t))

    lower_term =  T_i

    to_be_sqrt = upper_term/lower_term
    
    return np.sqrt(to_be_sqrt)

def formula_to_function(choice):
    funcs = {
            "FH": chapter7,
            "AO": asymptotically_optimal
        }
         
    func = funcs.get(choice)
    #print(func.__doc__)
    return func

#formula = "ao"
FORMULA_FUNC = None

ACTION = 0
REWARD = 1
N_K = 2

trace_len = 11340 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


initial_configuration = bandit_args["initial_configuration"]

def execute(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
    arms = bandit_args['arms']
    
    global FORMULA_FUNC
    FORMULA_FUNC = formula_to_function(formula) #this shouldn't be done every time

    
    knowledge = None
    #need an elegant way to handle the first read where knowledge doesn't exist yet
    if(bandit_args["knowledge"]):
        knowledge = bandit_args["knowledge"]
    else:
        action_reward_pairs = [ [arm, 0.0, 0.0] for arm in arms ] 
        bandit_args["knowledge"] = (-1, action_reward_pairs, arms.index(initial_configuration))
        knowledge = bandit_args["knowledge"]
    
    n_round = knowledge[0]
    action_reward_pairs = knowledge[1]
    last_action = knowledge[2]
    #knowledge = (round, action_reward_pairs)

    if((n_round + 1) < (len(arms))): #+1 because you are choosing the new action, which could be out of exploration range
        #initial exploration
        pair = action_reward_pairs[last_action]

        if(pair[ACTION] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(pair[ACTION]) + " is not reflected in SWIM's " + str((servers,dimmer)))

        reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
       
        pair[REWARD] = pair[REWARD] + sum(reward)
        pair[N_K] = pair[N_K] + 1
    
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
        total_count = sum([pair[N_K] for pair in action_reward_pairs])
        new_action = choose_action(action_reward_pairs,total_count)

        #don't really need to update the n_round anymore because we're out of initial exploration anyways
        new_knowledge = (n_round, action_reward_pairs, new_action)
        #save_to_pickle(new_knowledge, "ucb_knowledge")
        bandit_args['knowledge'] = new_knowledge

        return convert_conf(action_reward_pairs[new_action][ACTION],current_action[ACTION])


def choose_action(pairs, n):
    "Returns index in the pair list of the chosen action"

    highest = -99999999 # - sys.maxsize perhaps (python3 is unbounded)
    chosen_action = None

    # print("len pair")
    # print(str(len(pairs)))
    #print("Picking arm now")
    for pair_index in range(len(pairs)):
        
        current_pair = pairs[pair_index]

        Q_a = current_pair[REWARD]/current_pair[N_K]
    

        confidence = FORMULA_FUNC(current_pair, n)

        result = Q_a + confidence
        #print("Pair Index " + str(pair_index) + "has value " + str(result))
        if(result > highest): #and wf.criteria(current_pair[ACTION], wf)):
            #print("reached")
            highest = result
            chosen_action = pair_index

    # print("the value was " + str(highest))
    return chosen_action


    #sqrt( (np.log(n)/n_k) * 0.25 * ( (2 * np.log(n))/n_k) ) )

    

    


