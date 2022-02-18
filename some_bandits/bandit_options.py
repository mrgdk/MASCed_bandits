import random
import time
import itertools
bandit_args = {
    "start_time": round(time.time()),
    "arms": [],#[(4,1.0), (5,1.0), (10,1.0)],
    'cleaning': False,
    'stored_choice': None,
    "bandit_instance": None,
    "initial_configuration": None, #(4, 1.0),
    "shuffle": False,
    "record_decisions": True,
    "bounds": (175,230), #-400,300
    "utility_function": "SEAMS2022",
    "number_of_experts": 2,
    "preload_knowledge": False,
    "expert": "EXP3C",
    "round_counter": [0,0],
    "dynamic_bounds": False,
    "expert_preknowledge": [[36.608650878493556, 101.58972407707387, 155.44454636285019, 158.48317206373139, 160.14239383167592], 
                            [6.5191987585019859, 19.81411169769218, 41.438958866194355, -18.95283084856483, 126.99528063289736]]
}

if(bandit_args["shuffle"]) :random.shuffle(bandit_args["arms"])

