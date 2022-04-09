import unittest
from fractions import Fraction

from function.scalar_range_interpreter import ScalarRangeInterpreter
from tonalmodel.tonality import Tonality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_pitch import DiatonicPitch


class TestScalarRangeInterpreter(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_eval_as_nearest_pitch(self):
        print("------- test_eval_as_nearest_pitch")
        # Test for scalar range map
        tonality = Tonality.create(ModalityType.Major, 'C', 0)

        # 11 scalar notes to C:4 to G:5
        interpreter = ScalarRangeInterpreter(tonality, DiatonicPitch.parse('C:4'), 0, Fraction(1, 11))

        for i in range(0, 12):
            p = interpreter.eval_as_nearest_pitch(Fraction(i, 11))
            print('[{0}] {1}'.format(i, p))

        assert str(interpreter.eval_as_nearest_pitch(Fraction(0, 11))) == 'C:4'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(1, 11))) == 'D:4'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(2, 11))) == 'E:4'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(3, 11))) == 'F:4'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(4, 11))) == 'G:4'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(5, 11))) == 'A:4'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(6, 11))) == 'B:4'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(7, 11))) == 'C:5'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(8, 11))) == 'D:5'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(9, 11))) == 'E:5'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(10, 11))) == 'F:5'
        assert str(interpreter.eval_as_nearest_pitch(Fraction(11, 11))) == 'G:5'

        p = interpreter.eval_as_nearest_pitch(Fraction(3, 11) + 0.01)
        assert str(p) == 'F:4'

        p = interpreter.eval_as_nearest_pitch(Fraction(3, 11) + 0.08)
        assert str(p) == 'G:4'

    def test_value_for(self):
        print("------- test_value_for")

        tonality = Tonality.create(ModalityType.Major, 'E', 0)

        # 11 scalar notes to E:2 to E:3 increment scalar note per value increment of 1/10, with E:2 being 1
        interpreter = ScalarRangeInterpreter(tonality, DiatonicPitch.parse('E:2'), 1, Fraction(1, 10))

        for i in range(0, 8):
            p = interpreter.eval_as_nearest_pitch(1 + Fraction(i, 10))
            print('[{0}] {1} --> {2}'.format(i, p, interpreter.value_for(p)))

        assert interpreter.value_for(DiatonicPitch.parse('E:2')) == 1
        assert interpreter.value_for(DiatonicPitch.parse('F#:2')) == Fraction(11, 10)
        assert interpreter.value_for(DiatonicPitch.parse('G#:2')) == Fraction(12, 10)
        assert interpreter.value_for(DiatonicPitch.parse('A:2')) == Fraction(13, 10)
        assert interpreter.value_for(DiatonicPitch.parse('B:2')) == Fraction(14, 10)

        assert interpreter.value_for(DiatonicPitch.parse('F:2')) is None

    def test_book_example(self):
        print("------- test_book_example")
        # Test for scalar range map
        tonality = Tonality.create(ModalityType.Major, 'C', 0)

        # 11 scalar notes to C:4 to G:5
        interpreter = ScalarRangeInterpreter(tonality, DiatonicPitch.parse('C:4'), 0, Fraction(5, 2))

        for i in range(0, 12):
            p = interpreter.eval_as_nearest_pitch(Fraction(5 * i, 2))
            print('[{0}] {1}'.format(i, p))

    def test_book_example_1(self):
        print("------- test_book_example_1")
        tonality = Tonality.create(ModalityType.Major, 'E', 0)
        interpreter = ScalarRangeInterpreter(tonality, DiatonicPitch.parse('E:4'), 0, 1)

        for i in range(0, 8):
            p = interpreter.eval_as_nearest_pitch(i)
            print('[{0}] {1}'.format(i, p))

        gs_value = interpreter.value_for("G#:4")
        assert gs_value == 2
        gs_value = interpreter.value_for("G:4")
        assert gs_value is None

        pitches = interpreter.eval_as_pitch(5.2)
        print("[{0}]".format(', '.join(map(str, pitches))))
        assert pitches[0] == DiatonicPitch.parse('c#:5')
        assert pitches[1] == DiatonicPitch.parse('d#:5')

        assert 66 == interpreter.eval_as_accurate_chromatic_distance(8)  # 66 for F#:5
