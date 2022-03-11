# Abstract interface for a execution strategy
#
# An execution strategy that forms the logic of the experiment.
from some_bandits.bandit_options import bandit_args

class Bandit:
    def __init__(self, name):
        self.name = name
        if(bandit_args['arms']):
            self.arms = bandit_args['arms']
        else:
            print("no arms specified, in Bandit constructor")
            raise RuntimeError("No arms specified")
    def start_strategy(self, reward):
        """ starts execution """
        pass
    
    def visualize(self):
        """ will create a visualization of the current state of the algorithm """
        pass




