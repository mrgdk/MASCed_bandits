import numpy as np
from random import sample
from some_bandits.bandit_options import bandit_args
from some_bandits.utilities import convert_conf, save_to_pickle, calculate_utility
from some_bandits.bandits.Bandit import Bandit
from some_bandits.bandits.Expert import Expert
from statistics import mean


#ETA = 1
CUM_REWARD = 0
N_K = 1

class EwS(Bandit, Expert):
    def __init__(self, formula): 
        super().__init__("EwS-" + str(formula))
        self.weights, self.distribution = self.ews_initialize(len(self.arms))
        self.num_arms = len(self.arms)


        self.set_functions(formula)
        #np.random.seed(1337)
        self.arm_reward_pairs = {}
        for arm in self.arms: self.arm_reward_pairs[arm] = [0.0,0.0]
        
        self.last_action = bandit_args["initial_configuration"]
        self.distr_func()

           
    def ews_initialize(self, num_arms):
        return [0] * num_arms, []


    def start_strategy(self, reward):

        self.arm_reward_pairs[self.last_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[self.last_action][N_K]+=1



        
        self.update_func() #Update weights


        self.distr_func() #(re-)calculate Pt

        new_action = self.sample_action()
  
        self.last_action = self.arms[new_action]

        return self.arms[new_action]

    def distr_func(self):
        # exp(eta * S^_t-1i) / SUMkj=1 exp(eta * S^_t-1j)
        sum_weights = 0.0

        for i, arm in enumerate(self.arms):
            times_arm_played = self.arm_reward_pairs[arm][N_K]
            squared_gap = np.square(self.weights[i])
            sum_weights+= np.exp(-2*times_arm_played*squared_gap)

        self.distribution.clear()

        for i, arm in enumerate(self.arms):
            times_arm_played = self.arm_reward_pairs[arm][N_K]
            squared_gap = np.square(self.weights[i])
            self.distribution.append(np.exp(-2 * times_arm_played * squared_gap)/sum_weights)

    def update_func(self, payoff=None, action=None):
        empirical_gaps = None

        empirical_mean_rewards = []
        for arm in self.arms:
            current_entry = self.arm_reward_pairs[arm]
            if(current_entry[N_K] == 0):
                empirical_mean_rewards.append(0)
            else:
                empirical_mean_rewards.append(current_entry[CUM_REWARD]/current_entry[N_K])

        empirical_gaps = [max(empirical_mean_rewards) - emp_mean_rew for emp_mean_rew in empirical_mean_rewards]

        self.weights = empirical_gaps

    def propagate_reward(self, reward, chosen_action):
        self.arm_reward_pairs[chosen_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[chosen_action][N_K]+=1

        self.update_func()

        self.distr_func()
