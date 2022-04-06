import unittest
from fractions import Fraction

from function.chromatic_range_interpreter import ChromaticRangeInterpreter
from tonalmodel.diatonic_pitch import DiatonicPitch

class TestScalarRangeInterpreter(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_book_example(self):
        print("------- test_book_example")

        # 11 scalar notes to C:4 to C:5
        interpreter = ChromaticRangeInterpreter(DiatonicPitch.parse('C:4'), 0, Fraction(5, 2))

        for i in range(0, 7):
            p = interpreter.eval_as_nearest_pitch(Fraction(5 * i, 2))
            print('[{0}] {1}'.format(i, p))

        eb_value = interpreter.value_for("Eb:4")
        assert eb_value == Fraction(5 * 3, 2)

        pitches = interpreter.eval_as_pitch(3)
        print("[{0}]".format(', '.join(map(str, pitches))))
        assert pitches[0] == DiatonicPitch.parse('c#:4')
        assert pitches[1] == DiatonicPitch.parse('d:4')

        assert 50 == interpreter.eval_as_accurate_chromatic_distance(5)   # 50 for D:4