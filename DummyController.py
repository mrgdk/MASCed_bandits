from some_bandits.bandit_options import initialize_arguments
from some_bandits.bandits import init_bandit
import sys, os
from collections import Counter
from testing_unit import *
import pickle
import matplotlib.pyplot as plt
import imageio

ROUNDS = 100
BOUNDS = (0,100)
INITIAL_ARM = 0
SEED = 3
SAVE_DIR = "./records/"

NR_FILES = len([name for name in os.listdir(SAVE_DIR)])
PATH_NAME = SAVE_DIR + "run_" + str(NR_FILES)

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
    mytest.set_result(dict(coun), chosen_arms)
    save_run(mytest)
    visualize(chosen_arms,rewards)
    

def visualize(chosen_arms, rewards):
    plt.plot(chosen_arms, "-o")
    plt.title('Arm Selection Throughout the Run')
    plt.xlabel('Rounds')
    plt.ylabel('Arms')
    plt.savefig(PATH_NAME + '/arm_selection.png')
    plt.close()

    plt.plot(rewards, '-o')
    plt.title('Rewards Throughout the Run')
    plt.xlabel('Rounds')
    plt.ylabel('Rewards')
    plt.savefig(PATH_NAME + '/rewards.png')
    plt.close()
    
    create_gif(rewards)

    fig = plt.figure(figsize = (10,5))
    arms, counts = zip(*Counter(chosen_arms).items())
    plt.bar(arms, counts, color = 'maroon', width = 0.4)
    plt.xlabel("Arms")
    plt.ylabel("Counts")
    plt.title("Arm/Count Distribution")
    plt.savefig(PATH_NAME + '/arm_count_dist.png')
    plt.close()



def create_gif(rewards):
    filenames = []

    for i in range(-len(rewards) + 1, 1):
        plt.plot(rewards[:i])
        plt.title('Rewards Throughout the Run')
        plt.xlabel('Rounds')
        plt.ylabel('Rewards')
        filename = f'/{i}.png'
        filenames.append(filename)
        plt.savefig(PATH_NAME + filename)
        plt.close()

    with imageio.get_writer(PATH_NAME + '/reward_over_time.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(PATH_NAME +filename)
            writer.append_data(image)
    
    for filename in set(filenames):
        os.remove(PATH_NAME + filename)



def save_run(mytest):
    os.mkdir(PATH_NAME)

    with open(PATH_NAME + '/run.txt', 'w') as f:
        f.write(str(mytest))

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


start(sys.argv[1], sys.argv[2])