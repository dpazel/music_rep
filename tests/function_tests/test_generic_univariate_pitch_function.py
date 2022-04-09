import unittest
from fractions import Fraction
import math

from function.generic_univariate_pitch_function import GenericUnivariatePitchFunction
from function.chromatic_range_interpreter import ChromaticRangeInterpreter
from timemodel.position import Position
from tonalmodel.diatonic_pitch import DiatonicPitch


def local_sin(v):
    return math.sin(2 * math.pi * v)


class TestGenericUnivariatePitchFunction(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_gpf(self):
        f = GenericUnivariatePitchFunction(TestGenericUnivariatePitchFunction.square, Position(0), Position(2))

        factor = 32

        for i in range(0, factor + 1):
            p = Fraction(i, factor)
            d = f.eval_as_chromatic_distance(p)
            np = f.eval_as_nearest_pitch(p)
            choices = TestGenericUnivariatePitchFunction.print_choices(f.eval_as_pitch(p))
            txt = '[{0}] chrom={1} near_p={2}   choices={3}'.format(i, d, np, choices)
            print(txt)

        # test
        p = Fraction(25, factor)
        d = f.eval_as_chromatic_distance(p)
        np = f.eval_as_nearest_pitch(p)
        choices = f.eval_as_pitch(p)
        assert 2 == len(choices)
        assert 'C:4' == str(choices[0])
        assert 'C#:4' == str(choices[1])

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

        # test
        p = Fraction(5, factor)
        d = f.eval_as_chromatic_distance(p)
        np = f.eval_as_nearest_pitch(p)
        choices = f.eval_as_pitch(p)
        assert 2 == len(choices)
        assert 'D#:5' == str(choices[0])
        assert 'E:5' == str(choices[1])

    @staticmethod
    def square(value):
        return TestGenericUnivariatePitchFunction.BASE + value * value

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

    def test_book_example(self):
        # Interpreter 0__.C:4 and each step of 1/12 maps to noew chromatic
        interpreter = ChromaticRangeInterpreter(DiatonicPitch.parse('C:4'), 0, Fraction(1, 12))

        # local_sin maps 0->0 .25->1 .5->0 .75->-1 1->0 and so on.
        f = GenericUnivariatePitchFunction(local_sin, Position(0), Position(2), False, interpreter)

        for i in range(0, 9):
            p = f.eval_as_nearest_pitch(i * 0.25)
            print('[{0}] {1}'.format((i * 0.25), str(p)))


if __name__ == "__main__":
    unittest.main()
