import unittest

from misc.ordered_map import OrderedMap
from fractions import Fraction
from timemodel.position import Position
from timemodel.duration import Duration


class TestOrderedMap(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order(self):
        l = [(10, 100), (5, 20), (7, 70), (2, 50)]
        om = OrderedMap(l)
        keys = om.keys()
        last_key = -1
        for k in keys:
            print(k, om[k])
            self.assertTrue(last_key < k)
            last_key = k
            
        l = [(Fraction(2, 3), 200), (Fraction(1, 10), 10), (Fraction(1, 2), 50), (Fraction(1, 8), 20)]
        om = OrderedMap(l)
        keys = om.keys()
        last_key = -1
        for k in keys:
            print(k, om[k])
            self.assertTrue(last_key < k)
            last_key = k
            
        l = [(Position(2, 3), 200), (Position(1, 10), 10), (Position(1, 2), 50), (Position(1, 8), 20)]
        om = OrderedMap(l)
        keys = om.keys()
        last_key = -Fraction(1, 1)
        for k in keys:
            print(k, om[k])
            self.assertTrue(last_key < k.position)
            last_key = k.position
            
        l = [(Duration(2, 3), 200), (Duration(1, 10), 10), (Duration(1, 2), 50), (Duration(1, 8), 20)]
        om = OrderedMap(l)
        keys = om.keys()
        last_key = -Fraction(1, 1)
        for k in keys:
            print(k, om[k])
            self.assertTrue(last_key < k.duration)
            last_key = k.duration
            
    def test_insert(self):
        l = [(10, 100), (5, 20), (7, 70), (2, 50)]
        om = OrderedMap(l)        
        om.insert(6, 60)
        keys = om.keys()
        last_key = -1
        for k in keys:
            print(k, om[k])
            self.assertTrue(last_key < k)
            last_key = k
            
    def test_merge(self):
        l = [(10, 100), (5, 20), (7, 70), (2, 50)]
        om = OrderedMap(l)
        sup = [(3, 60), (15, 2)]
        om.merge(sup)
        self.assertTrue(3 in om.keys())
        self.assertTrue(om.get(3) == 60)
        self.assertTrue(15 in om.keys()) 
        self.assertTrue(om.get(15) == 2) 
        self.assertTrue(5 in om.keys())  
        
        sup = {3: 60, 15: 2}
        om.merge(sup)
        self.assertTrue(3 in om.keys())
        self.assertTrue(om.get(3) == 60)
        self.assertTrue(15 in om.keys()) 
        self.assertTrue(om.get(15) == 2) 
        self.assertTrue(5 in om.keys())  
        
        sup = OrderedMap({3: 60, 15: 2})
        om.merge(sup)
        self.assertTrue(3 in om.keys())
        self.assertTrue(om.get(3) == 60)
        self.assertTrue(15 in om.keys()) 
        self.assertTrue(om.get(15) == 2) 
        self.assertTrue(5 in om.keys())
        
    def test_floor(self):
        l = [(10, 100), (5, 20), (7, 70), (2, 50)]
        om = OrderedMap(l)
        answers = [2, 2, 2, 5, 5, 7, 7, 7, 10, 10]
        for i in range(2, 12):
            key = om.floor(i)
            self.assertTrue(key == answers[i - 2])
            mapto = om[key]
            print('find {0} is {1} --> {2}'.format(i, key, mapto))

    def test_ceil(self):
        l = [(10, 100), (5, 20), (7, 70), (2, 50)]
        om = OrderedMap(l)
        answers = [2, 5, 5, 5, 7, 7, 10, 10, 10, None, None]
        for i in range(1, 12):
            key = om.ceil(i)
            self.assertTrue(key == answers[i - 1])
            mapto = None if key is None else om[key]
            print('find {0} is {1} --> {2}'.format(i, key, mapto))
            
    def test_get(self):
        l = [(10, 100), (5, 20), (7, 70), (2, 50)]
        om = OrderedMap(l)
        
        a = om.get(5)
        assert a == 20
        
        from structure.time_signature import TimeSignature

        from timemodel.time_signature_event import TimeSignatureEvent
        tse = TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0))
        
        d = OrderedMap([(tse.time, tse)])
        x = d.get(0)
        assert x == tse
        
    def test_remove(self):
        l = [(10, 100), (5, 20), (7, 70), (2, 50)]
        om = OrderedMap(l)
        
        assert 5 in om
        
        assert om.get(5) == 20
        om.remove_key(5)
        assert 5 not in om

if __name__ == "__main__":
    unittest.main()
