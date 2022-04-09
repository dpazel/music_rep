import unittest
from function.generic_univariate_function import GenericUnivariateFunction


def square(x):
    return x * x


class TestGenericUnivariateFunction(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_function(self):
        f = GenericUnivariateFunction(square, -1, 5)
        
        assert f.eval(-1) == 1
        assert f.eval(0) == 0
        assert f.eval(1) == 1
        assert f.eval(2) == 4
        assert f.eval(3) == 9
        assert f.eval(4) == 16
        assert f.eval(5) == 25
        assert f.eval(6) == 36
    
    @staticmethod
    def square(x):
        return x*x
