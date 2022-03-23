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
    def __init__(self, num_of_rounds):
        self.arms = self.init_arms(get_configurations())
        self.num_arms = len(self.arms)
        self.rounds = num_of_rounds
    
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
        
        return arms
    
    """TODO: 
            ->Save the reward to a seed to generate the same thing later on.
    """
    #Generates reward for the specified arm.
    def generate_reward(self, arm):
        configs = self.arms[arm]
        dist_name = configs[0]
        reward = GENERATORS[dist_name](*configs[1:], size = 1)
        return reward
