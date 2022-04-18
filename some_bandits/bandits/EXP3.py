import numpy as np
from random import sample
from some_bandits.bandit_options import bandit_args
from some_bandits.utilities import convert_conf, save_to_pickle, calculate_utility
from some_bandits.bandits.Bandit import Bandit
from some_bandits.bandits.Expert import Expert
from statistics import mean

ACTION = 0
REWARD = 1
N_K = 2

#ETA = 1


class EXP3(Bandit, Expert):
    def __init__(self, formula): 
        super().__init__("EXP3-" + str(formula))
        self.weights, self.distribution = self.exp3_initialize(len(self.arms))
        self.num_arms = len(self.arms)
 
        #np.random.seed(1337)
        trace_len = 20000 #the total time of chosen trace in SWIM in seconds
        total_count = round(trace_len / 60) 
        self.eta = 0.1 #np.sqrt(np.log(len(self.arms)) / (len(self.arms) * total_count) ) #0.1
        
        self.last_action = bandit_args["initial_configuration"]
        self.distr_func()

        
        
       
    def exp3_initialize(self, num_arms):
        return [0] * num_arms, []

    


    def start_strategy(self, reward):
        #print("received this " + str(reward))

        #print("my distribution is ")
        #print(self.distribution)    
        
        self.update_func(reward, self.arms.index(self.last_action)) #Update weights

        ##print("now my weights are")
        #print(self.weights)
        self.distr_func() #(re-)calculate Pt
        
        #print("now my distribution is ")
        #print(self.distribution)     

        new_action = self.sample_action()
  
        self.last_action = self.arms[new_action]

        return self.arms[new_action]

    def propagate_reward(self, reward, chosen_action):
        self.update_func(reward, chosen_action)

        self.distr_func()

    # def formula_to_function(self, choice):
    #     funcs = {
    #             "FH": (fixed_horizon_Pt, fixed_horizon_up),
    #             "anytime": (anytime_Pt, anytime_up)
    #         }
            
    #     func = funcs.get(choice)
    #     ###print(func.__doc__)
    #     return func



    def distr_func(self):
        # exp(eta * S^_t-1i) / SUMkj=1 exp(eta * S^_t-1j)

        sum_weights = sum([np.exp(self.eta * weight) for weight in self.weights])

        self.distribution.clear()
        #P_t = 
        self.distribution.extend([np.exp(self.eta * weight)/sum_weights for weight in self.weights])

    def update_func(self, payoff, action):
        #S^_ti = S^_t-1i + 1 - I{A_t = i}(1 - X_t) / P_ti
        for weight_i in range(len(self.weights)):
            if(weight_i == action):
                self.weights[action] = self.weights[action] + 1 - ((1-payoff)/self.distribution[action]) 
            else:
                self.weights[weight_i] = self.weights[weight_i] + 1
        return
