import unittest
from function.constant_univariate_function import ConstantUnivariateFunction


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        f = ConstantUnivariateFunction(35, 2, 6)
        
        assert f.eval(2) == 35
        assert f.eval(3) == 35
        assert f.eval(6) == 35
        assert f.eval(7) == 35


if __name__ == "__main__":
    unittest.main()
