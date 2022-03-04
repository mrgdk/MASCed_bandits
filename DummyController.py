from some_bandits.bandit_options import initialize_arguments
from some_bandits.bandits import init_bandit
from numpy import random
import sys

ROUNDS = 100
ARMS = ["A1", "A2", "A2"]
BOUNDS = (0,100)
INITIAL_ARM = 0

def start(bandit_name, bandit_formula = ""):
    initialize_arguments(ARMS, INITIAL_ARM, bounds = BOUNDS)

    bandit_instance = init_bandit(bandit_name, bandit_formula)

    dist_per_arm = [random.rand] * len(ARMS)  # [random_function1, random_function2, random_function3]

    # initial round:
    reward = dist_per_arm[INITIAL_ARM]()
    # "start_strategy" means essentially "select_arm"
    chosen_arm = bandit_instance.start_strategy(reward)

    # rest of the rounds:
    for i in range(ROUNDS):
        # collect a reward
        reward = dist_per_arm[ARMS.index(chosen_arm)]()
        # ask the bandit for a new arm to play:
        chosen_arm = bandit_instance.start_strategy(reward)


start(sys.argv[1], sys.argv[2])