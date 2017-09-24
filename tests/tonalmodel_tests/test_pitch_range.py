import unittest
from tonalmodel.pitch_range import PitchRange
from tonalmodel.chromatic_scale import ChromaticScale


class TestPitchRange(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create(self):
        with self.assertRaises(Exception):
            PitchRange(8, 96)

        with self.assertRaises(Exception):
            PitchRange(9, 97)


        with self.assertRaises(Exception):
            PitchRange('Ab:0', 'C:8')

        with self.assertRaises(Exception):
            PitchRange.create('A:0', 'C#:8')

        
    def test_pitch_inbounds(self):
        pr = PitchRange.create('C:4', 'B:4')
        scale = list('CDEFGAB')
        for s in scale:
            self.assertTrue(pr.is_pitch_inbounds(s + ':4'))
        self.assertFalse(pr.is_pitch_inbounds('Cb:4'))
        self.assertFalse(pr.is_pitch_inbounds('B#:4'))
        
    def test_lowest_placement(self):
        pr = PitchRange.create('G:3', 'G:5')
        answers = [4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3]
        for i in range(0, 12):
            lowest = pr.find_lowest_placement_in_range(i)
            partition = ChromaticScale.index_to_location(lowest)[0]
            self.assertTrue(partition == answers[i], 'Assert failure {0} != {1}'.format(partition, answers[i]))
            print(i, partition)
            
        with self.assertRaises(Exception):
            pr.find_lowest_placement_in_range(-1)

        with self.assertRaises(Exception):
            pr.find_lowest_placement_in_range(12)

        
    def test_odd_ranges(self):
        pr = PitchRange.create('Cb:4', 'B#:4')
        print(str(pr))
        self.assertTrue(pr.start_index == 4 * 12 - 1)
        self.assertTrue(pr.end_index == 4 * 12 + 12)

if __name__ == "__main__":
    unittest.main()
