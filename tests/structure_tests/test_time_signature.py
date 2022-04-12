import unittest

from fractions import Fraction
from structure.time_signature import TSBeatType, TimeSignature
from timemodel.duration import Duration


class TSTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_TSBeatType(self):
        tsbt = TSBeatType(TSBeatType.Eighth)
        print(tsbt)
        f = tsbt.to_fraction()
        print(f)
        self.assertTrue(f == Fraction(1, 8))
        
        f = TSBeatType.get_fraction_for(TSBeatType.Sixteenth)
        self.assertTrue(f == Fraction(1, 16))
        f = TSBeatType.get_fraction_for(TSBeatType(TSBeatType.Sixteenth))
        self.assertTrue(f == Fraction(1, 16))
        
    def test_TimeSignature(self):
        ts = TimeSignature(5, Fraction(2, 3))
        self.assertTrue(ts.beats_per_measure == 5)
        self.assertTrue(ts.beat_duration == Fraction(2, 3))
        
        ts = TimeSignature(4, 6)
        self.assertTrue(ts.beats_per_measure == 4)
        self.assertTrue(ts.beat_duration == Fraction(6, 1))
        
        ts = TimeSignature(3, TSBeatType.Quarter)
        print(ts)
        self.assertTrue(ts.beats_per_measure == 3)
        print(ts.beats_per_measure == 3)
        self.assertTrue(ts.beat_duration == Fraction(1, 4))
        print(ts.beat_duration == Fraction(1, 4))
        
        ts = TimeSignature(7, Duration(8, 9))
        self.assertTrue(ts.beats_per_measure == 7)
        self.assertTrue(ts.beat_duration == Fraction(8, 9))
