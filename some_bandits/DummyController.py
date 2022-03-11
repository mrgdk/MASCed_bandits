from some_bandits.bandit_options import initialize_arguments
from some_bandits.bandits import init_bandit
from numpy import random
import sys

ROUNDS = 100
ARMS = ["A1", "A2", "A3"]
BOUNDS = (0,100)
INITIAL_ARM = 0

def start(bandit_name, bandit_formula=""):
    initialize_arguments(ARMS, INITIAL_ARM, bounds=BOUNDS)

    bandit_instance = init_bandit(bandit_name, bandit_formula)


    dist_per_arm = [random.rand] * len(ARMS)

    chosen_arm = bandit_instance.start_strategy(dist_per_arm[INITIAL_ARM]())
    for i in range(ROUNDS):
        chosen_arm = bandit_instance.start_strategy(dist_per_arm[ARMS.index(chosen_arm)]())
        
start(sys.argv[1], sys.argv[2])