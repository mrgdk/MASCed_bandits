import unittest
from TestController import *
from tests.normal import *
import pickle

class Test_egreedy(unittest.TestCase):
    def test_egreedy_normal_simple1(self):
        myMock = Mock(ROUNDS, seed1, "egreedy", 0.5)
        myMock.init_arms(normal_simple1)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed1, normal_simple1, "egreedy", 0.5))
    
    def test_egreedy_normal_simple2(self):
        myMock = Mock(ROUNDS, seed2, "egreedy", 0.5)
        myMock.init_arms(normal_simple2)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed2, normal_simple2, "egreedy", 0.5))
    
    def test_egreedy_binomial_simple1(self):
        myMock = Mock(ROUNDS, seed3, "egreedy", 0.5)
        myMock.init_arms(binomial_simple1)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed3, binomial_simple1, "egreedy", 0.5))
    
    def test_UCB_normal_simple1(self):
        myMock = Mock(ROUNDS, seed1, "UCB", "OG")
        myMock.init_arms(normal_simple1)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed1, normal_simple1, "UCB", "OG"))

    def test_UCBImproved_normal_simple1(self):
        myMock = Mock(ROUNDS, seed3, "UCBImproved", "OG")
        myMock.init_arms(normal_simple1)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed3, normal_simple1, "UCBImproved", "OG"))

    def test_UCBNorm_normal_simple2(self):
        myMock = Mock(ROUNDS, seed2, "UCBNorm", "OG")
        myMock.init_arms(normal_simple2)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed2, normal_simple2, "UCBNorm", "OG"))
    
    def test_SWUCB_binomial_simple1(self):
        myMock = Mock(ROUNDS, seed2, "SWUCB", 10)
        myMock.init_arms(binomial_simple1)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed2, binomial_simple1, "SWUCB", 10))
    
    def test_DUCB_binomial_simple1(self):
        myMock = Mock(ROUNDS, seed1, "DUCB", 0.5)
        myMock.init_arms(binomial_simple1)
        result = start(myMock)
        self.assertEqual(result, generate_result(seed1, binomial_simple1, "DUCB", 0.5))

    def test_previous_runs(self):
        prev_runs = []
        with open('record.pkl', 'rb+') as f:
            while True:
                try:
                    prev_runs.append(pickle.load(f))
                except EOFError:
                    break
        
        for run in prev_runs:
            myMock = Mock(ROUNDS, run.seed, run.bandit, run.formula)
            myMock.arms = run.arms
            result = start(myMock)
            self.assertEqual(result, run.get_result())
            