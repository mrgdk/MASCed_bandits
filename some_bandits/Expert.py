# Abstract interface for an expert to be used in EXP4
#
# Provides a distribution over some arms which can be updated and drawn from.
import numpy as np

class Expert:
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.distribution = None #should be initialized in subclass
        self.weights = None #should be initialized in subclass

    
    def say_hi(self):
        print("Hi i am an abstract expert")

    def sample_action(self):
        return np.random.choice(np.arange(0, self.num_arms), p= self.distribution)

    def propagate_reward(self, reward, chosen_action):
        'should be implemented in the subclass'
        pass
    



