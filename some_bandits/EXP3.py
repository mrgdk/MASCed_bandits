import numpy as np
from random import sample
from bandit_options import bandit_args
from utilities import convert_conf, save_to_pickle, calculate_utility

ACTION = 0
REWARD = 1
N_K = 2

#ETA = 1


LIST_OF_GAMES = []



DISTR_FUNC = None
UPDATE_FUNC = None

arms = bandit_args['arms']  
trace_len = 11340 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
ETA = np.sqrt(np.log(len(arms)) / (len(arms) * total_count) )

initial_configuration = bandit_args["initial_configuration"]

def execute(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
      
    #np.random.seed(1337)

    algorithm = "exp3"
    



    global DISTR_FUNC
    global UPDATE_FUNC
    (DISTR_FUNC, UPDATE_FUNC) = formula_to_function(formula)

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
        DISTR_FUNC(initial_PT, initial_Sweights)
        bandit_args["knowledge"] = (initial_Sweights, arms.index(initial_configuration), initial_PT)
        #(S_weights, last_conf, Pt)
        knowledge = bandit_args["knowledge"]
    

    #np.random.seed(seed)

    

    S_weights = knowledge[0]
    current_action_i = knowledge[1]
    P_t = knowledge[2]

    ########
    reward = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
    result_sum = sum(reward)

    UPDATE_FUNC(S_weights, current_action_i, P_t, result_sum) #Update weights

    DISTR_FUNC(P_t, S_weights) #(re-)calculate Pt
    
    new_action = np.random.choice(np.arange(0, len(arms)), p= P_t) #sample action from Pt
    
    #wf.primary_data_provider["last_action"] = current_action[ACTION]

    #####
    #don't really need to update the n_round anymore because we're out of initial exploration anyways
    new_knowledge = (S_weights, new_action, P_t)
     #save_to_pickle(new_knowledge, "ucb_knowledge")
    bandit_args['knowledge'] = new_knowledge

    if(bandit_args["record_decisions"]): 
        print("yayaya")
        save_to_pickle(new_knowledge, str(bandit_args["start_time"]))

    return convert_conf(arms[new_action],arms[current_action_i])


    
    

def formula_to_function(choice):
    funcs = {
            "FH": (fixed_horizon_Pt, fixed_horizon_up),
            "anytime": (anytime_Pt, anytime_up)
        }
         
    func = funcs.get(choice)
    #print(func.__doc__)
    return func



def fixed_horizon_Pt(P_ti, S_ti):
    #print("test")
    # exp(eta * S^_t-1i) / SUMkj=1 exp(eta * S^_t-1j)
    global ETA

    sum_weights = sum([np.exp(ETA * weight) for weight in S_ti])

    del P_ti[:] #P_ti.clear()
    #P_t = 
    P_ti.extend([np.exp(ETA * weight)/sum_weights for weight in S_ti])

def fixed_horizon_up(S_ti, A_t, P_t, payoff):
    #\print("test2")
    #S^_ti = S^_t-1i + 1 - I{A_t = i}(1 - X_t) / P_ti
    for weight_i in range(len(S_ti)):
        if(weight_i == A_t):
            S_ti[A_t] = S_ti[A_t] + 1 - ((1-payoff)/P_t[A_t]) 
        else:
            S_ti[weight_i] = S_ti[weight_i] + 1
    return


def anytime_Pt():
    # exp(-eta_t * SUMt-is=1 Y^_si ) / SUMkj=1 exp(-eta)

    return

def anytime_up(Y_ti, A_t, P_t, payoff):
    #Y^_ti = I{A_t = i}y_ti/P_ti

    Y_ti[A_t] = y_t[A_t]/P_t(A_t)