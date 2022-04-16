import unittest
import logging
from fractions import Fraction

from transformation.stepshift.t_stepshift import TStepShift, SecondaryShiftType, PitchRemapFunction
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from tonalmodel.diatonic_pitch import DiatonicPitch


class TestTStepShift(unittest.TestCase):
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_stepshift(self):
        print('----- test simple stepshift -----')

        line_text = '{<C-Major:I>qG:4 a b a g }'
        lge = LineGrammarExecutor()
        source_instance_line, source_instance_hct = lge.parse(line_text)

        trans = TStepShift(source_instance_line, source_instance_hct)
        new_line, new_hct = trans.apply(3)

        print_line(new_line)
        print_hct(new_hct)

        notes = new_line.get_all_notes()
        assert len(notes) == 5
        assert notes[0].diatonic_pitch == DiatonicPitch.parse('C:5')
        assert notes[1].diatonic_pitch == DiatonicPitch.parse('D:5')
        assert notes[2].diatonic_pitch == DiatonicPitch.parse('E:5')
        assert notes[3].diatonic_pitch == DiatonicPitch.parse('D:5')
        assert notes[4].diatonic_pitch == DiatonicPitch.parse('C:5')

        hclist = new_hct.hc_list()
        assert len(hclist) == 1
        assert str(hclist[0].tonality) == 'C-Major'
        assert hclist[0].chord.chord_template.scale_degree == 4
        assert str(hclist[0].chord.chord_type) == 'Maj'

    def test_secondary_chord_stepshift(self):
        print('----- test secondary chord stepshift -----')

        line_text = '{<C-Minor: IIIDom7/V-Melodic>qC:4 d eb f }'
        lge = LineGrammarExecutor()
        source_instance_line, source_instance_hct = lge.parse(line_text)

        # Keep change the chord and keep the denominator.
        trans = TStepShift(source_instance_line, source_instance_hct)
        new_line, new_hct = trans.apply(3)

        print_line(new_line)
        print_hct(new_hct)

        notes = new_line.get_all_notes()
        assert len(notes) == 4
        assert notes[0].diatonic_pitch == DiatonicPitch.parse('F#:4')
        assert notes[1].diatonic_pitch == DiatonicPitch.parse('G:4')
        assert notes[2].diatonic_pitch == DiatonicPitch.parse('Ab:4')
        assert notes[3].diatonic_pitch == DiatonicPitch.parse('Bbb:4')

        hclist = new_hct.hc_list()
        assert len(hclist) == 1
        assert str(hclist[0].tonality) == 'C-MelodicMinor'
        assert hclist[0].chord.chord_template.secondary_scale_degree == 5
        assert str(hclist[0].chord.secondary_tonality) == 'G-MelodicMinor'
        assert hclist[0].chord.primary_chord.chord_template.scale_degree == 6
        assert str(hclist[0].chord.chord_type) == 'Dom7'

        # Now keep the chord and change the denominator.
        trans = TStepShift(source_instance_line, source_instance_hct, SecondaryShiftType.Tonal)
        new_line, new_hct = trans.apply(3)

        print_line(new_line)
        print_hct(new_hct)

        hc_list = new_hct.hc_list()
        assert str(hc_list[0].chord) == 'TIIIDom7/I(MelodicMinor) [Eb, G, Bb, Db]'

    def test_unqualified_secondary(self):
        print('----- test unqualified secondary -----')

        line_text = '{<D-Major: VDom7/ii>qB:4 d f# a}'
        lge = LineGrammarExecutor()
        source_instance_line, source_instance_hct = lge.parse(line_text)
        print(source_instance_line)
        print(source_instance_hct)

        # Keep change the chord and keep the denominator.
        trans = TStepShift(source_instance_line, source_instance_hct, SecondaryShiftType.Tonal)
        new_line, new_hct = trans.apply(3)

        print_line(new_line)
        print_hct(new_hct)

    def test_multiple_hcs(self):
        print('----- test multiple hcs -----')

        line_text = '{<G-Major: ii> qC:4 d e f#  <G-Major: IV> C:5 e G:4 a <D-Major: I> b a g f# hd }'
        lge = LineGrammarExecutor()
        source_instance_line, source_instance_hct = lge.parse(line_text)

        trans = TStepShift(source_instance_line, source_instance_hct)
        new_line, new_hct = trans.apply(-1)

        print_line(new_line)
        print_hct(new_hct)

        notes = new_line.get_all_notes()
        assert len(notes) == 13
        assert notes[0].diatonic_pitch == DiatonicPitch.parse('B:3')
        assert notes[1].diatonic_pitch == DiatonicPitch.parse('C:4')
        assert notes[2].diatonic_pitch == DiatonicPitch.parse('D:4')
        assert notes[3].diatonic_pitch == DiatonicPitch.parse('E:4')
        assert notes[4].diatonic_pitch == DiatonicPitch.parse('B:4')
        assert notes[5].diatonic_pitch == DiatonicPitch.parse('D:5')
        assert notes[6].diatonic_pitch == DiatonicPitch.parse('F#:4')
        assert notes[7].diatonic_pitch == DiatonicPitch.parse('G:4')
        assert notes[8].diatonic_pitch == DiatonicPitch.parse('A:4')
        assert notes[9].diatonic_pitch == DiatonicPitch.parse('G:4')
        assert notes[10].diatonic_pitch == DiatonicPitch.parse('F#:4')
        assert notes[11].diatonic_pitch == DiatonicPitch.parse('E:4')
        assert notes[12].diatonic_pitch == DiatonicPitch.parse('C#:4')

        hc_list = new_hct.hc_list()
        assert str(hc_list[0].chord) == 'TIMaj [G, B, D]'
        assert str(hc_list[1].chord) == 'TIIIMin [B, D, F#]'
        assert str(hc_list[2].chord) == 'TVIIDim [C#, E, G]'

    def test_pitch_remap(self):
        print('----- test pitch remap -----')
        line_text = '{<Eb-Major: I> qC:4  }'
        lge = LineGrammarExecutor()
        source_instance_line, source_instance_hct = lge.parse(line_text)

        tonality = source_instance_hct.hc_list()[0].tonality

        fctn_map = PitchRemapFunction(tonality, 3)

        p = fctn_map[DiatonicPitch.parse('A#:4')]

        assert p == DiatonicPitch.parse('D##:5')


def print_line(line):
    notes = line.get_all_notes()
    for i in range(0, len(notes)):
        note = notes[i]
        print('[{0}]  {1}({2})'.format(i, note.diatonic_pitch, note.duration))


def print_hct(hct):
    hcs = hct.hc_list()
    count = 0
    for hc in hcs:
        print('[{0}] HC({1}, {2}, {3}, {4})'.format(count, hc.tonality, hc.chord, hc.duration, hc.position))
