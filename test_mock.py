import unittest
from TestController import *
from tests.normal import *
import pickle

class Test_egreedy(unittest.TestCase):
    bandit = "egreedy"
    formula = 0.5

    def test_normal_simple1(self):
        myMock = Mock(ROUNDS, seed1)
        myMock.init_arms(normal_simple1)
        result = start(self.bandit, self.formula, myMock)
        self.assertEqual(result, test_result1)
    
    def test_normal_simple2(self):
        myMock = Mock(ROUNDS, seed2)
        myMock.init_arms(normal_simple2)
        result = start(self.bandit, self.formula, myMock)
        self.assertEqual(result, test_result2)
    
    def test_binomial_simple1(self):
        myMock = Mock(ROUNDS, seed3)
        myMock.init_arms(binomial_simple1)
        result = start(self.bandit, self.formula, myMock)
        self.assertEqual(result, test_result3)
    
    def test_previous_runs(self):
        prev_runs = []
        with open('record.pkl', 'rb+') as f:
            while True:
                try:
                    prev_runs.append(pickle.load(f))
                except EOFError:
                    break
        
        for run in prev_runs:
            myMock = Mock(ROUNDS, run.seed)
            myMock.arms = run.arms
            result = start(self.bandit, self.formula, myMock)
            self.assertEqual(result, run.result)
        
        