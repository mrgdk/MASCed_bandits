# Abstract interface for a execution strategy
#
# An execution strategy that forms the logic of the experiment.


class Bandit:
    def __init__(self, formula):
        self.name = "defaultBanditName"
        
        
    def start_strategy(self, reward):
        """ starts execution """
        pass




