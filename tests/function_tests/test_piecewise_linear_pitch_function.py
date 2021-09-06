import unittest
from fractions import Fraction

import math

from function.piecewise_linear_pitch_function import PiecewiseLinearPitchFunction
from timemodel.position import Position
from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_pitch import DiatonicPitch


class TestPiecewiseLinearPitchFunction(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_plf(self):
        array = [(0, 'A:0'), (Fraction(1, 2), 'C:5'), (Position(3, 4), 'G:4'), (1, 'A:5')]
        f = PiecewiseLinearPitchFunction(array)

        assert DiatonicPitch.parse('A:0').chromatic_distance == f.eval(0)
        assert DiatonicPitch.parse('C:5').chromatic_distance == f.eval(0.5)
        assert DiatonicPitch.parse('G:4').chromatic_distance == f.eval(Fraction(3, 4))
        assert DiatonicPitch.parse('A:5').chromatic_distance == f.eval(Position(1))

        assert DiatonicPitch.parse('A:0').chromatic_distance == f.eval_as_chromatic_distance(0)
        assert DiatonicPitch.parse('C:5').chromatic_distance == f.eval_as_chromatic_distance(0.5)
        assert DiatonicPitch.parse('G:4').chromatic_distance == f.eval_as_chromatic_distance(Fraction(3, 4))
        assert DiatonicPitch.parse('A:5').chromatic_distance == f.eval_as_chromatic_distance(Position(1))


        print(f.eval_as_frequency(0))
        assert ChromaticScale.A0 == f.eval_as_frequency(0)

        print(ChromaticScale.index_to_location(DiatonicPitch.parse('C:5').chromatic_distance))
        print(ChromaticScale.get_frequency(ChromaticScale.index_to_location(DiatonicPitch.parse('C:5').chromatic_distance)))
        print(f.eval_as_frequency(0.5))
        assert math.isclose(ChromaticScale.get_frequency(
            ChromaticScale.index_to_location(DiatonicPitch.parse('C:5').chromatic_distance)),
            f.eval_as_frequency(0.5))

        print(f.eval(0.25))  # 34.5
        print(f.eval_as_nearest_pitch(0.25))
        assert math.isclose(
            ChromaticScale.A0 * math.pow(ChromaticScale.SEMITONE_RATIO, f.eval(0.25) - 9),
            f.eval_as_frequency(0.25))

        assert 'A#:2' == str(f.eval_as_nearest_pitch(0.25))

        pitches = f.eval_as_pitch(0.25)
        assert 'A#:2' == str(pitches[0])
        assert 'B:2' == str(pitches[1])

    def test_book_plf(self):
        array = [(0, 'A:4'), (Fraction(1, 2), 'C:5'), (Position(3, 4), 'e:4'), (1, 'C:5')]
        f = PiecewiseLinearPitchFunction(array)

        assert 'A:4' == str(f.eval_as_nearest_pitch(0))
        assert 'C:5' == str(f.eval_as_nearest_pitch(0.5))
        assert 'E:4' == str(f.eval_as_nearest_pitch(0.75))
        assert 'C:5' == str(f.eval_as_nearest_pitch(1))

        # Recall f is also an instnace of PiecewiseLinearFunction, so eval should work
        assert DiatonicPitch.parse('A:4').chromatic_distance == f.eval(0)
        assert DiatonicPitch.parse('C:5').chromatic_distance == f.eval(0.5)
        assert DiatonicPitch.parse('E:4').chromatic_distance == f.eval(Fraction(3, 4))
        assert DiatonicPitch.parse('C:5').chromatic_distance == f.eval(Position(1))

        # 0.25 has two tones that are considered close between A:4 and C:5
        print('[{0}]'.format(','.join(str(p) for p in f.eval_as_pitch(0.25))))

        # 0.625 between C:5 and E:4 comes to G#:4
        print('[{0}]'.format(','.join(str(p) for p in f.eval_as_pitch(Fraction(5,8)))))

        print(DiatonicPitch.parse('A:4').chromatic_distance)
        print( DiatonicPitch.parse('C:5').chromatic_distance)
        print( DiatonicPitch.parse('E:4').chromatic_distance)
        print( DiatonicPitch.parse('C:5').chromatic_distance)

