import unittest
from fractions import Fraction

from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from misc.interval import Interval


class TestLine(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sub_line(self):
        print('----- test_sub_line -----')

        source_instance_expression = '{<C-Major:I> qC:4 D E F <:v> [iD:5 B:4 A G] qC:5 D <:I> G:4 iF E hC}'
        lge = LineGrammarExecutor()

        source_instance_line, source_instance_hct = lge.parse(source_instance_expression)

        sub_line, start, duration = source_instance_line.sub_line(Interval(Fraction(1, 2), Fraction(2)))

        print(str(source_instance_line))
        print(str(sub_line))

        notes = sub_line.get_all_notes()
        assert notes is not None
        assert len(notes) == 8
        assert 'E:4' == str(notes[0].diatonic_pitch)
        assert 'F:4' == str(notes[1].diatonic_pitch)

        with self.assertRaises(Exception) as context:
            sub_line, start, duration = source_instance_line.sub_line(Interval(Fraction(1), Fraction(5, 4)))
            self.assertTrue('This is broken' in str(context.exception))

        sub_line, start, duration = source_instance_line.sub_line()

        print(str(source_instance_line))
        print(str(sub_line))

        assert sub_line.duration.duration == Fraction(3)