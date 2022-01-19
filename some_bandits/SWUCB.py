import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args



LOOK_BACK = 90

XI = 2

arms = bandit_args['arms']

initial_configuration = bandit_args["initial_configuration"]

def execute(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
   
    #establish base rewards

    knowledge = None
    #need an elegant way to handle the first read where knowledge doesn't exist yet
    if(bandit_args["knowledge"]):
        knowledge = bandit_args["knowledge"]
    else:
        bandit_args["knowledge"] = (-1, [], arms.index(initial_configuration))
        knowledge = bandit_args["knowledge"]
    
    n_round = knowledge[0]
    game_list = knowledge[1]
    last_action = knowledge[2]
    #knowledge = (round, action_reward_pairs)

    if((n_round + 1) < (len(arms))): #+1 because you are choosing the new action, which could be out of exploration range
        
        if(arms[last_action] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(arms[last_action]) + " is not reflected in SWIM's " + str((servers,dimmer)))

        reward_list = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)

        game_list.append((sum(reward_list)/len(reward_list), last_action)) #this represents the return of the evaluator() in definition.py and may need to be adjusted.

        n_round = n_round + 1

        new_knowledge = (n_round,game_list,n_round) #the round just also happens to be the index of action since we go through it one by one
        #save_to_pickle(new_knowledge, 'ucb_knowledge')
        bandit_args['knowledge'] = new_knowledge

        return convert_conf(arms[n_round], arms[last_action])
    else:
        #current_action = ARMS[action_index]
        if(arms[last_action] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(arms[last_action]) + " is not reflected in SWIM's " + str((servers,dimmer)))
        
        reward_list = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)

        game_list.append((sum(reward_list)/len(reward_list), last_action))

        action_index = choose_action(game_list)

        new_knowledge = (n_round, game_list, action_index)

        bandit_args['knowledge'] = new_knowledge

        return convert_conf(arms[action_index],arms[last_action])



def choose_action(game_list):
    global LOOK_BACK
    best_arm = None
    best_value = -9999999


    for arm_index in range(len(arms)):
        current_value = X_t(LOOK_BACK,arm_index,game_list) + c_t(LOOK_BACK, arm_index, game_list)
        if(current_value > best_value):
            best_value = current_value
            best_arm = arm_index
    
    return best_arm

def N_t(tau, i, game_list):

    total_count = len(game_list) #t
    
    start_point = max(0, total_count-tau+1)
    count = 0
    for game_index in range(start_point,total_count):
        if(game_list[game_index][1] == i): #I_s == i in other words arm of game equals given arm
            count += 1

    return count

def X_t(tau, i, game_list):
    total_count = len(game_list) #t
    summated = 0

    start_point = max(0, total_count-tau+1)
    for game_index in range(start_point,total_count):
        current_game = game_list[game_index]
        if(current_game[1] == i): #the games in which i was the arm
            X_s = current_game[0]

            summated+=X_s

    try:
        times_i_played = N_t(tau,i, game_list) 
        if(summated == 0 or times_i_played == 0): return 0
        
        return summated/N_t(tau,i, game_list)
    except:
        print("Divide by zero error likely")
        print(game_list)
        print("Last tau games are")
        print(game_list[-tau:])
        print("Length of game list is ")
        print(len(game_list))
        print("Result of N_t that was trigger is ")
        print(N_t(tau,i, game_list))
        print("and the arm causing it was ")
        print(i)
        print("Value of summated is ")
        print(summated)
        exit(1)

    
def c_t(tau, i, game_list):

    t = len(game_list)
    
    t_or_tau = min(t,tau)

    res = asymptotically_optimal(N_t(tau,i, game_list), t_or_tau)

    return res
 

def asymptotically_optimal(n_k, t):
    
    T_i = n_k

    f_t = 1 + (t  * np.square(np.log(t)))

    upper_term = 2 * (np.log(f_t))

    lower_term =  T_i

    to_be_sqrt = upper_term/lower_term
    
    return np.sqrt(to_be_sqrt)


def chapter7(n_k, n):
    delta = 1 / n^2

    upper_term = 2 * (np.log( (1 / delta) ))
    
    to_be_sqrt = upper_term/n_k
    
    return np.sqrt(to_be_sqrt)