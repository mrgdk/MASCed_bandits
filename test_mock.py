import unittest
from TestController import *
from tests.normal import *

class TestMock(unittest.TestCase):
    def test_normal_simple1(self):
        myMock = Mock(ROUNDS, seed1)
        myMock.init_arms(normal_simple1)
        result = start("egreedy", 0.5, myMock)
        self.assertEqual(result, test_result1)
    
    def test_normal_simple2(self):
        myMock = Mock(ROUNDS, seed2)
        myMock.init_arms(normal_simple2)
        result = start("egreedy", 0.5, myMock)
        self.assertEqual(result, test_result2)
    
    def test_binomial_simple1(self):
        myMock = Mock(ROUNDS, seed3)
        myMock.init_arms(binomial_simple1)
        result = start("egreedy", 0.5, myMock)
        self.assertEqual(result, test_result3)