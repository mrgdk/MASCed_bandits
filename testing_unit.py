from numpy import random
import functools
from input_config import *



GENERATORS = {
    "normal": random.normal,
    "binomial": random.binomial,
    "poisson": random.poisson,
    "bernoulli": functools.partial(random.binomial, 1),
    "exponential": random.exponential,
    "uniform": random.uniform
}


class Mock():

    def __init__(self, num_of_rounds, seed, bandit_name, bandit_formula):
        random.seed(seed)
        self.seed = seed
        self.arms = {}
        self.num_arms = len(self.arms)
        self.rounds = num_of_rounds
        self.bandit = bandit_name
        self.formula = bandit_formula
        self.result = {}
        self.arm_selections = []
    
    def __repr__(self) -> str:
        return "\nARMS:{}\nSEED:{}\nRESULT:{}\nSELECTIONS:{}".format(self.arms, self.seed, self.result, self.arm_selections)

    def __eq__(self, other):
        return self.seed == other.seed and self.arms == other.arms and self.arm_selections == other.arm_selections
    

    #Associates the arms with their configurations.
    def get_arms(self):
        return list(self.arms.keys())

    def init_arms(self, arms_info):
        arms = {}
        for i in range(len(arms_info)):
            current_arm = arms_info[i].split(" ")

            for j in range(1, len(current_arm)):
                current_arm[j] = float(current_arm[j])

            arms["A" + str(i+1)] = tuple(current_arm)
        
        self.arms = arms
    
    def set_result(self, arm_selection_freq, chosen_arms):
        self.result = arm_selection_freq
        self.arm_selections = chosen_arms
    
    def get_result(self):
        return (self.result, self.arm_selections)

    #Generates reward for the specified arm.
    def generate_reward(self, arm):
        configs = self.arms[arm]
        dist_name = configs[0]
        reward = GENERATORS[dist_name](*configs[1:], size = 1)
        return reward[0]
