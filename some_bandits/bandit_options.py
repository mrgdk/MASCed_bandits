import random
import time
import itertools
bandit_args = {
    "start_time": round(time.time()),
    #"arms": [(1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (7, 1.0), (8, 1.0), (9, 1.0), (10, 1.0)],
    "arms": [(1,1.0), (2,1.0), (3,1.0), (4,1.0), (5,1.0)],
    #"arms": None,
    "all_arms": False,
    'cleaning': False,
    'stored_choice': None,
    "knowledge": None,
    "initial_configuration": (3, 1.0),
    "shuffle": False,
    "record_decisions": True,
    "num_dim_levels": 3,
    "max_servers": 3,
    "bounds": (-400,300), #-400,300
    "utility_function": "SEAMS2022",
    "number_of_experts": 2,
    "preload_knowledge": True,
    "expert": "EXP3C",
    "round_counter": [0,0],
    "expert_preknowledge": [[36.608650878493556, 101.58972407707387, 155.44454636285019, 158.48317206373139, 160.14239383167592], 
                            [6.5191987585019859, 19.81411169769218, 41.438958866194355, -18.95283084856483, 126.99528063289736]]
}

if(bandit_args["shuffle"]) :random.shuffle(bandit_args["arms"])

if(bandit_args["all_arms"]):
    possible_dimmers = [(1.0 / (bandit_args["num_dim_levels"]-1)) * i for i in range(bandit_args["num_dim_levels"])]
    possible_servers = [j for j in range(1, bandit_args["max_servers"]+1)]
    all_combinations = list(itertools.product(possible_servers, possible_dimmers))
    bandit_args["arms"] = all_combinations

