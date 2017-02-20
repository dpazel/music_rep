import unittest
from function.piecewise_linear_function import PiecewiseLinearFunction


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_plf(self):
        array = [(5, 1), (7, 3), (10, 6), (12, 8)]
        f = PiecewiseLinearFunction(array)
        
        assert f.eval(0) == 1
        assert f.eval(2) == 1
        assert f.eval(5) == 1
        assert f.eval(6) == 2
        assert f.eval(7) == 3
        assert f.eval(8) == 4
        assert f.eval(9) == 5
        assert f.eval(10) == 6
        assert f.eval(11) == 7
        assert f.eval(11.5) == 7.5
        assert f.eval(12) == 8
        assert f.eval(13) == 8
        
    def test_one_tp(self):
        array = [(5, 1)]
        f = PiecewiseLinearFunction(array)    
        
        assert f.eval(0) == 1
        assert f.eval(2) == 1
        assert f.eval(5) == 1
        assert f.eval(6) == 1
        assert f.eval(7) == 1  
        
    def test_add_tp(self):
        array = [(5, 1), (7, 3), (10, 6), (12, 8)]
        f = PiecewiseLinearFunction(array)  
        
        f.add((15, 5))
        
        assert f.eval(0) == 1
        assert f.eval(2) == 1
        assert f.eval(5) == 1
        assert f.eval(6) == 2
        assert f.eval(7) == 3
        assert f.eval(8) == 4
        assert f.eval(9) == 5
        assert f.eval(10) == 6
        assert f.eval(11) == 7
        assert f.eval(11.5) == 7.5
        assert f.eval(12) == 8
        assert f.eval(13) == 7
        assert f.eval(14) == 6
        assert f.eval(15) == 5
        
        f.add_and_clear_forward((9, 5))
        assert f.eval(0) == 1
        assert f.eval(2) == 1
        assert f.eval(5) == 1
        assert f.eval(6) == 2
        assert f.eval(7) == 3
        assert f.eval(8) == 4
        assert f.eval(9) == 5
        assert f.eval(10) == 5
        assert f.eval(11) == 5
        assert f.eval(11.5) == 5
        assert f.eval(12) == 5
        assert f.eval(13) == 5
        assert f.eval(14) == 5
        assert f.eval(15) == 5


if __name__ == "__main__":
    unittest.main()
