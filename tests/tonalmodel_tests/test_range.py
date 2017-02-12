import unittest
from tonalmodel.range import Range


class TestRange(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create(self):
        with self.assertRaises(Exception) as context:
            Range(1.2, 5)
        print context.exception
        with self.assertRaises(Exception) as context:
            Range(8, 12.25)
        print context.exception
        with self.assertRaises(Exception) as context:
            Range(30, 25)
        print context.exception
        
    def test_inbounds(self):
        ranger = Range(12, 40)
        for i in range(12, 41):
            self.assertTrue(ranger.is_inbounds(i), '{0} is not in {1}'.format(i, ranger))
        self.assertFalse(ranger.is_inbounds(11))
        self.assertFalse(ranger.is_inbounds(41))
        
        self.assertTrue(ranger.is_inbounds(20.56))
        self.assertFalse(ranger.is_inbounds(11.999999))
        
    def test_attributes(self):
        ranger = Range(10, 20)
        self.assertTrue(ranger.size() == 11)
        self.assertTrue(ranger.start_index == 10)
        self.assertTrue(ranger.end_index == 20)
        
        ranger = Range(10, 10)
        self.assertTrue(ranger.size() == 1)
        self.assertTrue(ranger.start_index == 10)
        self.assertTrue(ranger.end_index == 10)
        self.assertTrue(ranger.is_inbounds(10))

if __name__ == "__main__":
    unittest.main()
