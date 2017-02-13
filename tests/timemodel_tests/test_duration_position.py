import unittest
from fractions import Fraction

from timemodel.duration import Duration
from timemodel.position import Position


class DurationPositionTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_duration(self):
        # d = d + x
        d1 = Duration(1, 2)
        assert d1.duration == Fraction(1, 2)
        d2 = d1 + Fraction(1, 4)
        assert d2.duration == Fraction(3, 4)
        
        d1 = Duration(1, 2)
        d2 = d1 + 2
        assert d2.duration == Fraction(5, 2)
        
        d1 = Duration(1, 2)
        d2 = d1 + Duration(Fraction(3, 4))
        print 'd1={0} d2 = {1}, d2 type = {2}'.format(d1, d2, type(d2))
        assert d2.duration == Fraction(5, 4)
        
        # d = x + d
        d1 = Duration(1, 2)
        assert d1.duration == Fraction(1, 2)
        d2 = Fraction(1, 4) + d1
        assert d2.duration == Fraction(3, 4)
        
        d1 = Duration(1, 2)
        d2 = 2 + d1
        assert d2.duration == Fraction(5, 2)

        d1 = Duration(1, 2)
        d2 = Duration(Fraction(3, 4)) + d1
        print 'd1={0} d2 = {1}, d2 type = {2}'.format(d1, d2, type(d2))
        assert d2.duration == Fraction(5, 4)               
        
        # d += x
        d1 = Duration(1, 2)
        d1 += Fraction(1, 4)
        assert d1.duration == Fraction(3, 4)
        
        d1 = Duration(1, 2)
        d1 += 2
        assert d1.duration == Fraction(5, 2)
        
        d1 = Duration(1, 2)
        d1 += Duration(1, 4)
        assert d1.duration == Fraction(3, 4)
        
        # d = d - x
        d1 = Duration(1, 2)
        assert d1.duration == Fraction(1, 2)
        d2 = d1 - Fraction(1, 4)
        assert d2.duration == Fraction(1, 4)
        
        d1 = Duration(3, 2)
        d2 = d1 - 1
        assert d2.duration == Fraction(1, 2)
        
        d1 = Duration(1, 1)
        d2 = d1 - Duration(Fraction(3, 4))
        print 'd1={0} d2 = {1}, d2 type = {2}'.format(d1, d2, type(d2))
        assert d2.duration == Fraction(1, 4)
        
        # d = x - d
        d1 = Duration(1, 2)
        assert d1.duration == Fraction(1, 2)
        d2 = Fraction(1, 4) - d1
        assert d2.duration == -Fraction(1, 4)
        
        d1 = Duration(3, 2)
        d2 = 1 - d1
        assert d2.duration == -Fraction(1, 2)
        
        # d = -d
        d1 = Duration(8, 9)
        d2 = -d1
        assert d2.duration == -Fraction(8, 9)
        
        # d -= x
        d1 = Duration(1, 2)
        d1 -= Fraction(1, 4)
        assert d1.duration == Fraction(1, 4)
        
        d1 = Duration(1, 2)
        d1 -= 2
        assert d1.duration == -Fraction(3, 2)
        
        d1 = Duration(1, 2)
        d1 -= Duration(1, 4)
        assert d1.duration == Fraction(1, 4)
        
        # d = d * x
        d1 = Duration(1, 2)
        d2 = d1 * Fraction(1, 4)
        assert d2.duration == Fraction(1, 8)
        
        d1 = Duration(1, 2)
        d2 = d1 * 2
        assert d2.duration == Fraction(1, 1)
        
        d1 = Duration(1, 2)
        with self.assertRaises(Exception) as context:
            d1 * Duration(Fraction(3, 4))
        self.assertTrue('* operator' in context.exception.message)   
        
        # d = d * x
        d1 = Duration(1, 2)
        d2 = Fraction(1, 4) * d1
        assert d2.duration == Fraction(1, 8)
        
        d1 = Duration(1, 2)
        d2 = 2 * d1
        assert d2.duration == Fraction(1, 1)   
        
        # d *=  x
        d1 = Duration(1, 2)
        d1 *= Fraction(1, 4)
        assert d1.duration == Fraction(1, 8)
        
        d1 = Duration(1, 2)
        d1 *= 2
        assert d1.duration == Fraction(1, 1)  
        
    def test_position(self):
        
        # p = p + x
        p1 = Position(3, 4)
        p2 = p1 + Fraction(1, 2)
        assert p2.position == Fraction(5, 4)
        
        p1 = Position(3, 4)
        p2 = p1 + 1
        assert p2.position == Fraction(7, 4)
        
        p = Position(2, 1)
        p1 = p + 1
        assert p1.position == Fraction(3, 1)
        
        p1 = Position(15, 16)
        assert p1.position == Fraction(15, 16)
        p2 = p1 + Duration(1, 8) 
        print 'p1={0} p2 = {1}, p2 type = {2}'.format(p1, p2, type(p2))
        assert p2.position == Fraction(17, 16)
      
        # p = p - x
        p1 = Position(3, 4)
        p2 = p1 - Fraction(1, 2)
        assert p2.position == Fraction(1, 4)
        
        p1 = Position(7, 4)
        p2 = p1 - 1
        assert p2.position == Fraction(3, 4)
        
        p1 = Position(15, 16)
        assert p1.position == Fraction(15, 16)
        p2 = p1 - Duration(1, 8) 
        print 'p1={0} p2 = {1}, p2 type = {2}'.format(p1, p2, type(p2))
        assert p2.position == Fraction(13, 16)
        
        # p += x
        p1 = Position(3, 4)
        p1 += 1
        assert p1.position == Fraction(7, 4)
        
        p1 = Position(3, 4)
        p1 += Fraction(1, 4)
        assert p1.position == Fraction(1, 1)
        
        p1 = Position(3, 4)
        p1 += Duration(1, 4)
        assert p1.position == Fraction(1, 1)
        
        d1 = Duration(1, 2)
        with self.assertRaises(Exception) as context:
            d1 += Position(1, 4)
        assert '+= operator' in context.exception.message
        
        # p = x + p         
        p1 = Position(3, 4)
        p2 = Fraction(1, 2) + p1
        assert p2.position == Fraction(5, 4)
        
        p1 = Position(3, 4)
        p2 = 1 + p1
        assert p2.position == Fraction(7, 4)
        
        p1 = Position(15, 16)
        p2 = Duration(Fraction(1, 8)) + p1 
        print 'p1={0} p2 = {1}, p2 type = {2}'.format(p1, p2, type(p2))
        assert p2.position == Fraction(17, 16)
        
        p1 = Position(1, 2)
        with self.assertRaises(Exception) as context:
            p1 + Position(1, 4)
        self.assertTrue('+ operator' in context.exception.message)
        
        # p = p - x
        p1 = Position(3, 4)
        p2 = p1 - 1
        assert p2.position == -Fraction(1, 4)
        
        p1 = Position(3, 4)
        p2 = p1 - Fraction(1, 4)
        assert p2.position == Fraction(1, 2)
        
        p1 = Position(3, 4)
        p2 = p1 - Duration(1, 2)
        assert p2.position == Fraction(1, 4)
        
        p1 = Position(3, 4)
        d = p1 - Position(1, 2)
        assert d.duration == Fraction(1, 4)
        
        # p -= x
        p1 = Position(3, 4)
        p1 -= 1
        assert p1.position == -Fraction(1, 4)
        
        p1 = Position(3, 4)
        p1 -= Fraction(1, 2)
        assert p1.position == Fraction(1, 4)

        p1 = Position(3, 4)
        p1 -= Duration(1, 2)
        assert p1.position == Fraction(1, 4)   

    def test_negate(self):
        d = Duration(4, 5)
        e = -d
        print 'd={0} e={1}'.format(d, e)
        assert e.duration == -Fraction(4, 5)

    def test_dots(self):
        d = Duration(1, 2)
        
        d0 = d.apply_dots(0)
        assert d0.duration == d
        
        d1 = d.apply_dots(1)
        assert d1.duration == Fraction(3, 4)
        
        d2 = d.apply_dots(2)
        assert d2.duration == Fraction(7, 8)


if __name__ == "__main__":
    unittest.main()
