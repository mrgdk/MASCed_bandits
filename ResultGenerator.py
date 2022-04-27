#generate_result(seed1, normal_simple1, "egreedy", 0.3)
from TestController import *
import pickle

class ResultGenerator():
    def __init__(self):
        self.run_to_result = {}

        buffer = {}
        with open('test_results.pkl', 'rb+') as f:
            buffer = pickle.load(f)
        print("Read {} test cases".format(len(buffer)))
        self.run_to_result = buffer


    #Generates results using the given seed, distribution, bandit name and the formula.
    def generate(self, seed, arms, bandit, formula):
        mymock = Mock(ROUNDS, seed, bandit, formula)
        mymock.init_arms(arms)
        run = tuple([seed, tuple(arms), bandit, formula])
        self.run_to_result[run] = start(mymock)

    def get_result(self, seed, arms, bandit, formula):
        run = tuple([seed, tuple(arms), bandit, formula])
        return self.run_to_result[run]

    def save_result(self):
        with open('test_results.pkl', 'wb') as f:
            pickle.dump(self.run_to_result, file = f)


mygenerator = ResultGenerator()

mygenerator.generate(seed1, normal_simple1, "egreedy", 0.3)
mygenerator.generate(seed2, normal_simple2, "egreedy", 0.1)
mygenerator.generate(seed3, binomial_simple1, "egreedy", 0.2)
mygenerator.generate(seed1, normal_simple1, "UCB", "OG")
mygenerator.generate(seed3, normal_simple1, "UCBImproved", "OG")
mygenerator.generate(seed2, normal_simple2, "UCBNorm", "OG")
mygenerator.generate(seed2, binomial_simple1, "SWUCB", 10)
mygenerator.generate(seed1, binomial_simple1, "DUCB", 0.5)
mygenerator.generate(seed1, normal_simple1, "EwS", "")
mygenerator.generate(seed1, binomial_simple2, "EXP3", 0.5)
mygenerator.generate(seed3, binomial_simple2, "EXP3S", 0.6)
mygenerator.generate(seed3, binomial_simple2, "EXP4", 0.9)

mygenerator.save_result()

