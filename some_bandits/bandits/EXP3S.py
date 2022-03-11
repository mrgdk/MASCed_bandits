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


class EXP3S(Bandit, Expert):
    def __init__(self, formula): 
        super().__init__("EXP3S-" + formula)
        self.weights, self.distribution = self.exp3s_initialize(len(self.arms))
        self.num_arms = len(self.arms)

        #np.random.seed(1337)
        trace_len = 2000 #the total time of chosen trace in SWIM in seconds
        total_count = 1000#round(trace_len / 60) 
        self.gamma = 0.5 #1/total_count
        self.alpha = 0.0001#min(1, np.sqrt( (self.num_arms * np.log(self.num_arms * total_count)) / total_count))
        #alpha is the learning rate, the lower it is the harder the probabilities commit. If you set it too high you will get overflowing weights
        #gamma is the discount factor
        #low gamma entails your new reward has slight influence on weights but the weight affects the dsitribution heavily
        #high gamma entails your new reward influences the weights but the weights don't affect the distribution
        self.last_action = bandit_args["initial_configuration"]
        self.distr_func()

        
        
       
    def exp3s_initialize(self, num_arms):
        return [1] * num_arms, []



    def start_strategy(self, reward):
        #print("received this " + str(reward))

        #print("my distribution is ")
        #print(self.distribution)    
        
        self.update_func(reward, self.last_action) #Update weights

        #print("now my weights are")
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

    def formula_to_function(self, choice):
        funcs = {
                "FH": (fixed_horizon_Pt, fixed_horizon_up),
                "anytime": (anytime_Pt, anytime_up)
            }
            
        func = funcs.get(choice)
        ##print(func.__doc__)
        return func



    def distr_func(self):
        # exp(eta * S^_t-1i) / SUMkj=1 exp(eta * S^_t-1j)

        sum_weights = sum(self.weights)


        self.distribution.clear()
        #P_t = 
        self.distribution.extend([(1 - self.gamma) * (weight/sum_weights) + (self.gamma/self.num_arms) for weight in self.weights])


    def update_func(self, reward, chosen_action):
        # print("making new weights")
        # print("the distribution is")
        # print(self.distribution)
        reward_estimates = [0] * len(self.arms)

        chosen_arm_i = self.arms.index(chosen_action)

        reward_estimates[chosen_arm_i] = reward/self.distribution[chosen_arm_i]
        # print("rew estimates")
        # print(reward_estimates)
        sum_prev_weights = sum(self.weights)
        #print("prev weight sum")
        #print(sum_prev_weights)

        #print("prev weights are")
        #print(self.weights)
        for weight_i in range(len(self.weights)):
            prev_weight = self.weights[weight_i]
            #print("gamma is " + str(self.gamma))
            leftside = prev_weight * np.exp(self.gamma * reward_estimates[weight_i] / self.num_arms)
            #print("left side is ")
            #print(leftside)
            rightside = ((np.exp(1) * self.alpha) / self.num_arms) * sum_prev_weights
            #print("alpha is ")
            #print(self.alpha)
            #print("right side is ")
            #print(rightside)
            self.weights[weight_i] = leftside + rightside #new weight


