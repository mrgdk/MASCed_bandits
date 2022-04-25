from some_bandits.bandit_options import initialize_arguments
from some_bandits.bandits import init_bandit
import sys
from collections import Counter
from testing_unit import *
import pickle
import matplotlib.pyplot as plt

ROUNDS = 100
BOUNDS = (0,100)
INITIAL_ARM = 0
SEED = 3

def start(bandit_name, bandit_formula = ""):
    mytest = Mock(ROUNDS, SEED, bandit_name, bandit_formula)
    mytest.init_arms(get_configurations())
    ARMS = mytest.get_arms()
    
    initialize_arguments(ARMS, INITIAL_ARM, bounds = BOUNDS)
    bandit_instance = init_bandit(bandit_name, bandit_formula)

    # initial round:
    reward = mytest.generate_reward(ARMS[INITIAL_ARM])
    chosen_arm = bandit_instance.start_strategy(reward)
    
    # rest of the rounds:
    chosen_arms = []
    rewards = []
    for i in range(mytest.rounds):
        reward = mytest.generate_reward(chosen_arm)
        chosen_arm = bandit_instance.start_strategy(reward)
        chosen_arms += [chosen_arm]
        rewards += [reward]
    
    coun = Counter(chosen_arms)
    
    for k in coun.keys():
        coun[k] /= len(chosen_arms)

    """TODO: DONT TOUCH ABOVE!!!"""

    #Setting the result of the run and selected arms by far in the mock object and saving this run in my record file.
    print(dict(coun))
    mytest.set_result(dict(coun), chosen_arms)
    save_run(mytest)
    visualize(chosen_arms,rewards)
    


def visualize(chosen_arms, rewards):
    plt.plot(chosen_arms, "-o")
    plt.title('Arm Selection Throughout the Run')
    plt.xlabel('Rounds')
    plt.ylabel('Arms')
    plt.savefig('arm_selection.png')
    plt.show()

    plt.plot(rewards, '-ok')
    plt.title('Rewards Throughout the Run')
    plt.xlabel('Rounds')
    plt.ylabel('Rewards')
    plt.savefig('rewards.png')
    plt.show()

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
    else:
        print("\n\n\nPREVIOUSLY YOU HAVE RUN THIS!!!\n\n\n")


start(sys.argv[1], sys.argv[2])