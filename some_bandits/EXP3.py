from hashlib import new
import numpy as np
from random import sample
from bandit_options import bandit_args
from utilities import convert_conf, save_to_pickle, calculate_utility
from Bandit import Bandit
from Expert import Expert

ACTION = 0
REWARD = 1
N_K = 2

#ETA = 1


class EXP3C(Bandit, Expert):
    def __init__(self):
        self.arms = bandit_args["arms"]
        self.num_arms = len(self.arms)
        self.knowledge = None
        bandit_args["bounds"] = (-400,300)
        self.weights, self.distribution = self.exp3_initialize(len(self.arms))

        self.distr_func = None
        self.update_func = None

        
        trace_len = 15000 #the total time of chosen trace in SWIM in seconds
        total_count = round(trace_len / 60) 
        self.eta = np.sqrt(np.log(len(self.arms)) / (len(self.arms) * total_count) )
        
        
    def exp3_initialize(self, num_arms):
        return [0] * num_arms, []

    def set_functions(self, formula):
        self.distr_func, self.update_func = self.formula_to_function(formula)


    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        #print(0)
        #np.random.seed(1337)
        print(bandit_args["bounds"])
        self.set_functions(formula)

        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
            #print("grabbed old knowledge")
        else:
            #print("initialized knowledge")
            initial_configuration = bandit_args["initial_configuration"]
            self.distr_func(self.distribution, self.weights, self.eta)
            bandit_args["knowledge"] = (self.weights, self.arms.index(initial_configuration), self.distribution)
            #(S_weights, last_conf, Pt)
            self.knowledge = bandit_args["knowledge"]
 
        #print(1)
        #np.random.seed(seed)

        self.weights = []
        self.distribution = []

        self.weights.extend(self.knowledge[0])
        current_action_i = self.knowledge[1]
        self.distribution.extend(self.knowledge[2])

        #print(2)

        ########
        reward, _ , _  = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
        #print('reward received')
        #print(reward)
        result_sum = sum(reward)

        self.update_func(self.weights, current_action_i, self.distribution, result_sum) #Update weights

        self.distr_func(self.distribution, self.weights, self.eta) #(re-)calculate Pt
        #print(3)
        
        new_action = self.sample_action()
        #print("new action is")
        #print(new_action)
        #wf.primary_data_provider["last_action"] = current_action[ACTION]

        #####
        #don't really need to update the n_round anymore because we're out of initial exploration anyways
        new_knowledge = (self.weights, new_action, self.distribution)
        #save_to_pickle(new_knowledge, "ucb_knowledge")
        bandit_args['knowledge'] = new_knowledge
        #print(4)

        if(bandit_args["record_decisions"]): 
            save_to_pickle(new_knowledge, "exp3_" + str(bandit_args["start_time"]))

        #print(5)

        return convert_conf(self.arms[new_action],self.arms[current_action_i])

    def propagate_reward(self, reward, chosen_action):
        self.update_func(self.weights, chosen_action, self.distribution, reward)

        self.distr_func(self.distribution, self.weights, self.eta)

    def formula_to_function(self, choice):
        funcs = {
                "FH": (fixed_horizon_Pt, fixed_horizon_up),
                "anytime": (anytime_Pt, anytime_up)
            }
            
        func = funcs.get(choice)
        ##print(func.__doc__)
        return func



def fixed_horizon_Pt(P_ti, S_ti, eta):
    # exp(eta * S^_t-1i) / SUMkj=1 exp(eta * S^_t-1j)

    sum_weights = sum([np.exp(eta * weight) for weight in S_ti])

    del P_ti[:] #P_ti.clear()
    #P_t = 
    P_ti.extend([np.exp(eta * weight)/sum_weights for weight in S_ti])

def fixed_horizon_up(S_ti, A_t, P_t, payoff):
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
