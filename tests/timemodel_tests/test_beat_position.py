import unittest
from timemodel.beat_position import BeatPosition


class TestBeatDuration(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order(self):
        bp = BeatPosition(5, 2)
        print(bp)
        self.assertTrue(str(bp) == 'BP[5, 2]')
        
        # ==
        bp1 = BeatPosition(5, 2)
        self.assertTrue(bp == bp1)
        
        # <
        bp1 = BeatPosition(4, 5)
        self.assertTrue(bp > bp1)
        
        bp1 = BeatPosition(5, 1)
        self.assertTrue(bp > bp1)
        
        # >=
        bp1 = BeatPosition(5, 2)
        self.assertTrue(bp >= bp1)
        
        bp1 = BeatPosition(4, 5)
        self.assertTrue(bp >= bp1)
        
        bp1 = BeatPosition(5, 1)
        self.assertTrue(bp >= bp1)
        
        # <=
        bp1 = BeatPosition(5, 2)
        self.assertTrue(bp <= bp1)
        
        bp1 = BeatPosition(5, 5)
        self.assertTrue(bp <= bp1)
        
        bp1 = BeatPosition(6, 1)
        self.assertTrue(bp <= bp1)
        
        # <        
        bp1 = BeatPosition(5, 5)
        self.assertTrue(bp < bp1)
        
        bp1 = BeatPosition(6, 1)
        self.assertTrue(bp < bp1)
