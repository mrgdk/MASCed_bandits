import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args


#formula = "ao"
FORMULA_FUNC = None

REWARD = 0
ACTION = 1



trace_len = 11340 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


initial_configuration = bandit_args["initial_configuration"]
class randomexploreC():
    def __init__(self):
        self.arms = bandit_args['arms']
        self.prev_config = bandit_args["initial_configuration"]
        
        
        
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        new_choice = self.arms[np.random.choice(np.arange(0, len(self.arms)))]
        old_choice = self.prev_config

        bandit_args["initial_configuration"] = old_choice
        return convert_conf(new_choice, old_choice)





 


       
        



