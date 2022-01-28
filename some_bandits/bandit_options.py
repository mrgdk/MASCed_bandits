import random
import time
import itertools
bandit_args = {
    "start_time": round(time.time()),
    #"arms": [(1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (7, 1.0), (8, 1.0), (9, 1.0), (10, 1.0)],
    "arms": [(3,1.0), (2,1.0), (1,1.0)],
    #"arms": None,
    "all_arms": False,
    "knowledge": None,
    "initial_configuration": (2, 1.0),
    "shuffle": False,
    "record_decisions": False,
    "num_dim_levels": 3,
    "max_servers": 3,
    "bounds": (0,1), #-400,300
    "utility_function": "SEAMS2022",
    "number_of_experts": 2,
    "preload_knowledge": True,
    "expert": "EXP3C",
    "expert_preknowledge": [[129.02386770425622, 
                            123.8327023149118, 
                            59.420433221853855, 
                            119.93483569447329, 
                            132.46199736250193, 
                            136.57383548027616, 
                            133.88170447222652, 
                            109.09659018688946, 
                            131.23666949599502], 
                            [164.36104445412539, 
                            -1.3204926697745094, 
                            69.967788059595961, 
                            153.43786384591465, 
                            -8.9342000109323223, 
                            106.94988870805373, 
                            150.40174410897131, 
                            113.53877098175438, 
                            91.335522715236294]]
}

if(bandit_args["shuffle"]) :random.shuffle(bandit_args["arms"])

if(bandit_args["all_arms"]):
    possible_dimmers = [(1.0 / (bandit_args["num_dim_levels"]-1)) * i for i in range(bandit_args["num_dim_levels"])]
    possible_servers = [j for j in range(1, bandit_args["max_servers"]+1)]
    all_combinations = list(itertools.product(possible_servers, possible_dimmers))
    bandit_args["arms"] = all_combinations

