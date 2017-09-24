import unittest
from misc.interval import Interval, BoundaryPolicy
from fractions import Fraction

import logging


class TestInterval(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_simple_equals(self):
        int_interval = Interval(5, 9)
       
        assert int_interval == Interval(5, 9)

        assert int_interval != Interval(5, 9, BoundaryPolicy.Closed)
        assert int_interval == Interval(5, 9, BoundaryPolicy.HI_Open)
        assert int_interval != Interval(4, 7)

    def test_simple_interval(self):
        int_interval = Interval(5, 9)
    
        assert int_interval.contains(7)
        assert int_interval.contains(6)
    
        assert Interval.intersects(int_interval, Interval(7, 10))
        assert int_interval.intersection(Interval(7, 10)) == Interval(7, 9).intersection(int_interval)
        
    def test_boundary(self):
        f_interval = Interval(Fraction(1, 4), Fraction(3, 5))   
        assert f_interval.contains(Fraction(1, 4))
        assert not f_interval.contains(Fraction(3, 5))
    
        f_interval = Interval(Fraction(1, 4), Fraction(3, 5), BoundaryPolicy.Open)
        assert not f_interval.contains(Fraction(1, 4))
        assert not f_interval.contains(Fraction(3, 5))
    
        f_interval = Interval(Fraction(1, 4), Fraction(3, 5), BoundaryPolicy.Closed)
        assert f_interval.contains(Fraction(1, 4))
        assert f_interval.contains(Fraction(3, 5))
    
        f_interval = Interval(Fraction(1, 4), Fraction(3, 5), BoundaryPolicy.LO_Open)
        assert not f_interval.contains(Fraction(1, 4))
        assert f_interval.contains(Fraction(3, 5))
        
    def test_intersection_boundary(self):
        interval = Interval(1, 5, BoundaryPolicy.Open).intersection(Interval(4, 6, BoundaryPolicy.Open))
        logging.info('{0}'.format(interval))
        assert interval.policy == BoundaryPolicy.Open
        
        interval = Interval(1, 5, BoundaryPolicy.Closed).intersection(Interval(4, 6, BoundaryPolicy.Closed))
        logging.info('{0}'.format(interval))
        assert interval.policy == BoundaryPolicy.Closed
        
        interval = Interval(1, 5, BoundaryPolicy.Open).intersection(Interval(4, 6, BoundaryPolicy.Closed))
        logging.info('{0}'.format(interval))
        assert interval.policy == BoundaryPolicy.HI_Open
        
        interval = Interval(1, 5, BoundaryPolicy.Closed).intersection(Interval(4, 6, BoundaryPolicy.Open))
        logging.info('{0}'.format(interval))
        assert interval.policy == BoundaryPolicy.LO_Open
    

if __name__ == "__main__":
    unittest.main()
