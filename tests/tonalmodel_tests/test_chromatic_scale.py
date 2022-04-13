import unittest
import logging

from tonalmodel.chromatic_scale import ChromaticScale


class TestChromaticScale(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_frequencies(self):
        assert is_close(ChromaticScale.get_frequency((4, 9)), 440.0), \
            "Error A:4 = {0} should be 440.0".format(ChromaticScale.get_frequency((4, 9)))
        assert is_close(ChromaticScale.get_frequency((4, 0)), 261.625565301), \
            "Error C:4 = {0} should be 261.625565301".format(ChromaticScale.get_frequency((4, 0)))
        
    def test_parse_chromatic_location(self):
        for i in range(0, 12):
            s = str(4) + ':' + str(i)
            location = ChromaticScale.parse_notation(s)  
            assert location[0] == 4 and location[1] == i
            
    def test_location_to_index(self):
        for i in range(1, 4):
            for j in range(0, 12):
                index = ChromaticScale.location_to_index((i, j))
                assert index == 12 * i + j
                
    def test_index_to_location(self):
        for i in range(12, 47):
            location = ChromaticScale.index_to_location(i)
            logging.info(location)
            assert location[0] == i // 12 and location[1] == i % 12
            
    def test_scale(self):
        scale = ChromaticScale.get_chromatic_scale(ChromaticScale.parse_notation("0:9"),
                                                   ChromaticScale.parse_notation("8:0"))
        start = ChromaticScale.location_to_index((0, 9))
        end = ChromaticScale.location_to_index((8, 0)) + 1
    
        for i in range(start, end):
            logging.info('{0}{1}   {1}'.format(i, ChromaticScale.index_to_location(i),  scale[i - start]))
            
        assert is_close(scale[ChromaticScale.location_to_index((4, 9)) - start], 440.0), \
            "Error A:4 = {0} should be 440.0".format(scale[ChromaticScale.location_to_index((4, 9)) - start])
        assert is_close(scale[ChromaticScale.location_to_index((4, 0)) - start], 261.625565301), \
            "Error C:4 = {0} should be 261.625565301".format(scale[ChromaticScale.location_to_index((4, 0)) - start])

    def test_book_example(self):
        location = ChromaticScale.parse_notation("4:9")
        print(location)
        index = ChromaticScale.location_to_index(location)
        print(index)
        loc = ChromaticScale.index_to_location(index)
        print(loc)


def is_close(value_a, value_b):
    return abs(value_a - value_b) < 0.0001


def is_close_in_bounds(value_a, value_b, tolerance):
    return abs(value_a - value_b) < tolerance
