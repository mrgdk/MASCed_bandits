from some_bandits.bandit_options import initialize_arguments
from some_bandits.bandits import init_bandit
import sys
from collections import Counter
from testing_unit import *
import pickle


ROUNDS = 100
BOUNDS = (0,100)
INITIAL_ARM = 0
SEED = 3

def start(bandit_name, bandit_formula = ""):
    mytest = Mock(ROUNDS,SEED)
    mytest.init_arms(get_configurations())
    ARMS = mytest.get_arms()
    
    initialize_arguments(ARMS, INITIAL_ARM, bounds = BOUNDS)
    bandit_instance = init_bandit(bandit_name, bandit_formula)

    # initial round:
    reward = mytest.generate_reward(ARMS[INITIAL_ARM])
    chosen_arm = bandit_instance.start_strategy(reward)
    
    # rest of the rounds:
    chosen_arms = []
    for i in range(mytest.rounds):
        reward = mytest.generate_reward(chosen_arm)
        chosen_arm = bandit_instance.start_strategy(reward)
        chosen_arms += [chosen_arm]
    
    coun = Counter(chosen_arms)
    
    for k in coun.keys():
        coun[k] /= len(chosen_arms)

    """TODO: DONT TOUCH ABOVE!!!"""

    mytest.result = dict(coun)

    save_run(mytest)

"""TODO: """

def save_run(mytest):
    loaded_dict = []

    with open('record.pkl', 'rb+') as f:
        while True:
            try:
                loaded_dict.append(pickle.load(f))
            except EOFError:
                break
    
    if not mytest in loaded_dict:
        with open('record.pkl', 'ab') as f:
            pickle.dump((mytest), file = f)
    print(loaded_dict)


start(sys.argv[1], sys.argv[2])