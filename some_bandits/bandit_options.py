import random
import time
import itertools
bandit_args = {
    "start_time": round(time.time()),
    #"arms": [(1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (7, 1.0), (8, 1.0), (9, 1.0), (10, 1.0)],
    "arms": None,
    "all_arms": True,
    "knowledge": None,
    "initial_configuration": (2, 0.5),
    "shuffle": False,
    "record_decisions": False,
    "num_dim_levels": 3,
    "max_servers": 3,
    "bounds": (20,200),
    "utility_function": "SEAMS2022"
}

if(bandit_args["shuffle"]) :random.shuffle(bandit_args["arms"])

if(bandit_args["all_arms"]):
    possible_dimmers = [(1.0 / (bandit_args["num_dim_levels"]-1)) * i for i in range(bandit_args["num_dim_levels"])]
    possible_servers = [j for j in range(1, bandit_args["max_servers"]+1)]
    all_combinations = list(itertools.product(possible_servers, possible_dimmers))
    bandit_args["arms"] = all_combinations

