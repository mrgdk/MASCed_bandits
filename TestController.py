from some_bandits.bandit_options import initialize_arguments
from some_bandits.bandits import init_bandit
import sys
from collections import Counter
from testing_unit import *
from distribution.normal import *

ROUNDS = 100
BOUNDS = (0,100)
INITIAL_ARM = 0

def start(myMock):
    ARMS = myMock.get_arms()
    initialize_arguments(ARMS, INITIAL_ARM, bounds = BOUNDS)
    bandit_instance = init_bandit(myMock.bandit, myMock.formula)
    reward = myMock.generate_reward(ARMS[INITIAL_ARM])
    chosen_arm = bandit_instance.start_strategy(reward)
    
    chosen_arms = []
    for i in range(ROUNDS):
        reward = myMock.generate_reward(chosen_arm)
        chosen_arm = bandit_instance.start_strategy(reward)
        chosen_arms += [chosen_arm]
    
    coun = Counter(chosen_arms)
    
    for k in coun.keys():
        coun[k] /= len(chosen_arms)
    
    return (dict(coun), chosen_arms)