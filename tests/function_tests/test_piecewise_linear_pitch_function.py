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

        print(f.eval(0))
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
