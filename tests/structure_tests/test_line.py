import unittest
from fractions import Fraction

from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.line import Line
from misc.interval import Interval
from structure.note import Note
from timemodel.duration import Duration
from timemodel.offset import Offset
from tonalmodel.diatonic_pitch import DiatonicPitch


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

    def test_pin(self):
        print('----- test_pin -----')

        l1_notes = [Note(DiatonicPitch(4, y), Duration(1, 8)) for y in 'abcd']
        l2_notes = [Note(DiatonicPitch(4, y), Duration(1, 8)) for y in 'efgab']
        line = Line()
        line.pin(Line(l1_notes), Offset(1, 8))
        line.pin(Line(l2_notes), Offset(1, 4))

        N = line.get_all_notes();
        print('... pinned notes ...')
        for n in N:
            print('({0}) : {1}'.format(n.get_absolute_position(), n.diatonic_pitch))
        print ('... end pinned notes ...')

        print('End test_pin')

    def test_book_example(self):
        print('----- book_example -----')

        voice_line = Line()
        melody_line = Line()

        melody_1 = Line([Note(DiatonicPitch(4, y), Duration(1, 8)) for y in 'aceg'])
        melody_2 = Line([Note(DiatonicPitch(4, y), Duration(1, 8)) for y in 'cadg'])
        base_line = Line([Note(DiatonicPitch(4, y), Duration(1, 4)) for y in 'dddddddd'])

        melody_line.pin(melody_1, Offset(1, 8))
        melody_line.pin(melody_2, Offset(1, 4))
        voice_line.pin(melody_line)
        voice_line.pin(base_line)

        print(voice_line)

        N = voice_line.get_all_notes();
        print('... pinned notes ...')
        for n in N:
            print('({0}) : {1}'.format(n.get_absolute_position(), n.diatonic_pitch))
        print ('... end pinned notes ...')

        print('End test_pin')