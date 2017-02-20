import unittest
from function.stepwise_function import StepwiseFunction


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_setups(self):
        array = [(5, 1), (7, 2), (10, 1.5), (12, 38)]
        f = StepwiseFunction(array)
        
        assert f.eval(0) == 1
        assert f.eval(2) == 1
        assert f.eval(5) == 1
        assert f.eval(6) == 1
        assert f.eval(7) == 2
        assert f.eval(8) == 2
        assert f.eval(9) == 2
        assert f.eval(10) == 1.5
        assert f.eval(11) == 1.5
        assert f.eval(11.99999) == 1.5
        assert f.eval(12) == 38
        assert f.eval(13) == 38
        
    def test_add_points(self):
        array = [(5, 1), (7, 2), (10, 1.5), (12, 38)]
        f = StepwiseFunction(array)
        
        f.add((8, 15))    
        
        assert f.eval(0) == 1
        assert f.eval(2) == 1
        assert f.eval(5) == 1
        assert f.eval(6) == 1
        assert f.eval(7) == 2
        assert f.eval(8) == 15
        assert f.eval(9) == 15
        assert f.eval(10) == 1.5
        assert f.eval(11) == 1.5
        assert f.eval(11.99999) == 1.5
        assert f.eval(12) == 38
        assert f.eval(13) == 38  
        
        f.add((2, 30))  
        assert f.eval(0) == 30
        assert f.eval(0) == 30
        assert f.eval(2) == 30
        assert f.eval(3) == 30
        assert f.eval(5) == 1
        assert f.eval(6) == 1
        assert f.eval(7) == 2
        assert f.eval(8) == 15
        assert f.eval(9) == 15
        assert f.eval(10) == 1.5
        assert f.eval(11) == 1.5
        assert f.eval(11.99999) == 1.5
        assert f.eval(12) == 38
        assert f.eval(13) == 38
        
        f.add_and_clear_forward((8, 35))
        assert f.eval(0) == 30
        assert f.eval(0) == 30
        assert f.eval(2) == 30
        assert f.eval(3) == 30
        assert f.eval(5) == 1
        assert f.eval(6) == 1
        assert f.eval(7) == 2
        assert f.eval(8) == 35
        assert f.eval(9) == 35
        assert f.eval(10) == 35
        assert f.eval(11) == 35
        assert f.eval(11.99999) == 35
        assert f.eval(12) == 35
        assert f.eval(13) == 35


if __name__ == "__main__":
    unittest.main()
