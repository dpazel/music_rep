import unittest
from timemodel.position import Position


class TestPosition(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_increment(self):
        p = Position(1)
        print p
        p += 1
        print p
        assert p.position == 2
        p += 1
        print p
        assert p.position == 3
        
        p = 2 - p
        print p
        assert p.position == -1


if __name__ == "__main__":
    unittest.main()
