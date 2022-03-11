
import numpy as np
import time
from some_bandits.utilities import calculate_utility, convert_conf
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits.Bandit import Bandit

DECAY_RATE = 1

REWARD = 0
ACTION = 1
class egreedy(Bandit):
    def __init__(self, formula):
        super().__init__("e-greedy")
        #self.formula = self.formula_to_function(formula)

        initial_configuration = bandit_args["initial_configuration"]
        self.game_list = []
        self.last_action = initial_configuration

        self.epsilon = float(formula)

    def start_strategy(self, reward):
        self.game_list.append([reward, self.last_action])
        
        choice = np.random.random()

        if choice < self.epsilon: new_action = self.arms[np.random.choice(len(self.arms))]
        else: new_action = max(self.arms, key=lambda arm: self.reward_average(arm))

        self.epsilon = self.epsilon/DECAY_RATE
        self.last_action = new_action
        return new_action


    def reward_average(self, arm):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == arm): #the games in which arm was chosen
                r_sum+=game[REWARD]
     
        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played
    
    def times_played(self, arm):
        return len([game for game in self.game_list if game[ACTION] == arm])




    

    


