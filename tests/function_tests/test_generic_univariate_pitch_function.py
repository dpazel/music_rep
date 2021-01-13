import unittest
from fractions import Fraction

import math

from function.generic_univariate_pitch_function import GenericUnivariatePitchFunction
from timemodel.position import Position
from tonalmodel.diatonic_pitch import DiatonicPitch


class TestGenericUnivariatePitchFunction(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_gpf(self):
        f = GenericUnivariatePitchFunction(TestGenericUnivariatePitchFunction.square, Position(0), Position(2))

    def test_generic_sin(self):
        f = GenericUnivariatePitchFunction(TestGenericUnivariatePitchFunction.sinasoidal, Position(0), Position(2))

        factor = 32

        for i in range(0, factor + 1):
            p = Fraction(i, factor)
            d = f.eval_as_chromatic_distance(p)
            np = f.eval_as_nearest_pitch(p)
            choices = TestGenericUnivariatePitchFunction.print_choices(f.eval_as_pitch(p))
            txt = '[{0}] chrom={1} near_p={2}   choices={3}'.format(i, d, np, choices)
            print(txt)

    @staticmethod
    def square(x):
        return x*x

    BASE = DiatonicPitch.parse('C:4').chromatic_distance

    @staticmethod
    def sinasoidal(v):
        return TestGenericUnivariatePitchFunction.BASE + 19 * math.sin(2 * math.pi * v)

    @staticmethod
    def print_choices(choices):
        if len(choices) == 1:
            return '({0})'.format(choices)
        else:
            return '({0}, {1})'.format(choices[0], choices[1])


if __name__ == "__main__":
    unittest.main()
