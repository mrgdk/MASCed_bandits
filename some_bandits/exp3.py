
import numpy as np
import time
import pickle
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args



def formula_to_function(choice):
    funcs = {
            "IEEESASO2019": IEEESASO2019,
            "chap_7": chapter7,
            "ao": asymptotically_optimal
        }
         
    func = funcs.get(choice)
    #print(func.__doc__)
    return func

formula = "ao"
FORMULA_FUNC = formula_to_function(formula)

ACTION = 0
REWARD = 1
N_K = 2



initial_configuration = bandit_args["initial_configuration"]

def execute(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate):
    arms = bandit_args['arms']

    #global FORMULA_FUNC
    #FORMULA_FUNC = formula_to_function(formula) #this shouldn't be done every time

    
    knowledge = None
    #need an elegant way to handle the first read where knowledge doesn't exist yet
    if(bandit_args["knowledge"]):
        knowledge = bandit_args["knowledge"]
    else:
        action_reward_pairs = [ [arm, 0.0, 0.0] for arm in arms ] 
        bandit_args["knowledge"] = (0, action_reward_pairs, arms.index(initial_configuration))
        knowledge = bandit_args["knowledge"]
    
    n_round = knowledge[0]
    action_reward_pairs = knowledge[1]
    last_action = knowledge[2]
    #knowledge = (round, action_reward_pairs)

    if((n_round +1) < (len(arms))): #+1 because you are choosing the new action, which could be out of exploration range
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
        #print("yea")
        #action_index = choose_action(wf,action_reward_pairs,total_count)
        action_index = last_action
        #index_picks.append(action_index)


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



def get_results(values_to_collect, wf, action):
    while(True): 
        #this loop was added to deal with no_metric or ValueError
        # time.sleep(wf.execution_strategy["collection_window"])

        result = arm_experiment(wf,action)
        #print(result)
        values_to_collect.extend(result)  
        if(wf.execution_strategy["isExperimentValid"]):
            break
        else:
            if len(values_to_collect) >= wf.execution_strategy["sample_points"]:
                break

        #result = (dummy_rewards[pair_count],0)
    sample_list = sample(values_to_collect, wf.execution_strategy["sample_points"])
    values_to_collect.clear()
    values_to_collect.extend(sample_list)



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

    

    


