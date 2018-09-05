import unittest

from harmonicmodel.secondary_chord_template import SecondaryChordTemplate
from harmonicmodel.tertian_chord_template import TertianChordTemplate, TertianChordType
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.beam import Beam
from structure.tuplet import Tuplet
from timemodel.duration import Duration


class TestTuplet(unittest.TestCase):
    ORIGINAL_TEST = '{ <E-Major:iv> C:5 D Eb F (1:8, 2)[C:3 D:4 E] <:v> [i@C#:3 sBb D:4 Fbb]}'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_note_identities(self):
        print('----- test_note_identities -----')

        l = LineGrammarExecutor()

        s = '{C:4 D:4 E:4 F:4 G:4 A:4 B:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert 'C:4' == str(notes[0].diatonic_pitch)
        assert 'D:4' == str(notes[1].diatonic_pitch)
        assert 'E:4' == str(notes[2].diatonic_pitch)
        assert 'F:4' == str(notes[3].diatonic_pitch)
        assert 'G:4' == str(notes[4].diatonic_pitch)
        assert 'A:4' == str(notes[5].diatonic_pitch)
        assert 'B:4' == str(notes[6].diatonic_pitch)

        s = '{c:4 d:4 e:4 f:4 g:4 a:4 b:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert 'C:4' == str(notes[0].diatonic_pitch)
        assert 'D:4' == str(notes[1].diatonic_pitch)
        assert 'E:4' == str(notes[2].diatonic_pitch)
        assert 'F:4' == str(notes[3].diatonic_pitch)
        assert 'G:4' == str(notes[4].diatonic_pitch)
        assert 'A:4' == str(notes[5].diatonic_pitch)
        assert 'B:4' == str(notes[6].diatonic_pitch)

        s = '{Cb:4 Db:4 Eb:4 Fb:4 Gb:4 Ab:4 Bb:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert 'Cb:4' == str(notes[0].diatonic_pitch)
        assert 'Db:4' == str(notes[1].diatonic_pitch)
        assert 'Eb:4' == str(notes[2].diatonic_pitch)
        assert 'Fb:4' == str(notes[3].diatonic_pitch)
        assert 'Gb:4' == str(notes[4].diatonic_pitch)
        assert 'Ab:4' == str(notes[5].diatonic_pitch)
        assert 'Bb:4' == str(notes[6].diatonic_pitch)

        s = '{Cbb:4 Dbb:4 Ebb:4 Fbb:4 Gbb:4 Abb:4 Bbb:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert 'Cbb:4' == str(notes[0].diatonic_pitch)
        assert 'Dbb:4' == str(notes[1].diatonic_pitch)
        assert 'Ebb:4' == str(notes[2].diatonic_pitch)
        assert 'Fbb:4' == str(notes[3].diatonic_pitch)
        assert 'Gbb:4' == str(notes[4].diatonic_pitch)
        assert 'Abb:4' == str(notes[5].diatonic_pitch)
        assert 'Bbb:4' == str(notes[6].diatonic_pitch)

        s = '{C#:4 D#:4 E#:4 F#:4 G#:4 A#:4 B#:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert 'C#:4' == str(notes[0].diatonic_pitch)
        assert 'D#:4' == str(notes[1].diatonic_pitch)
        assert 'E#:4' == str(notes[2].diatonic_pitch)
        assert 'F#:4' == str(notes[3].diatonic_pitch)
        assert 'G#:4' == str(notes[4].diatonic_pitch)
        assert 'A#:4' == str(notes[5].diatonic_pitch)
        assert 'B#:4' == str(notes[6].diatonic_pitch)

        s = '{C##:4 D##:4 E##:4 F##:4 G##:4 A##:4 B##:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert 'C##:4' == str(notes[0].diatonic_pitch)
        assert 'D##:4' == str(notes[1].diatonic_pitch)
        assert 'E##:4' == str(notes[2].diatonic_pitch)
        assert 'F##:4' == str(notes[3].diatonic_pitch)
        assert 'G##:4' == str(notes[4].diatonic_pitch)
        assert 'A##:4' == str(notes[5].diatonic_pitch)
        assert 'B##:4' == str(notes[6].diatonic_pitch)

    def test_durations(self):
        print('----- test_durations -----')
        l = LineGrammarExecutor()

        s = '{wC:4 hD:4 qE:4 iF:4 sG:4 tA:4 xB:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert Duration(1) == notes[0].duration
        assert Duration(1, 2) == notes[1].duration
        assert Duration(1, 4) == notes[2].duration
        assert Duration(1, 8) == notes[3].duration
        assert Duration(1, 16) == notes[4].duration
        assert Duration(1, 32) == notes[5].duration
        assert Duration(1, 64) == notes[6].duration

        s = '{WC:4 HD:4 QE:4 IF:4 SG:4 TA:4 XB:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert Duration(1) == notes[0].duration
        assert Duration(1, 2) == notes[1].duration
        assert Duration(1, 4) == notes[2].duration
        assert Duration(1, 8) == notes[3].duration
        assert Duration(1, 16) == notes[4].duration
        assert Duration(1, 32) == notes[5].duration
        assert Duration(1, 64) == notes[6].duration

        s = '{(2:1)C:4 (3:2)D:4 (4:3)E:4}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.get_all_notes()
        assert Duration(2, 1) == notes[0].duration
        assert Duration(3, 2) == notes[1].duration
        assert Duration(4, 3) == notes[2].duration

    def test_beam(self):
        print('----- test_beam -----')
        l = LineGrammarExecutor()

        s = '{qC:4 D:4 [E:3 F G A B:4]}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.sub_notes
        assert len(notes) == 3
        assert 'C:4' == str(notes[0].diatonic_pitch)
        assert 'D:4' == str(notes[1].diatonic_pitch)
        assert isinstance(notes[2], Beam)
        beam = notes[2]
        b_notes = beam.sub_notes
        assert len(b_notes) == 5
        assert 'E:3' == str(b_notes[0].diatonic_pitch)
        assert 'F:3' == str(b_notes[1].diatonic_pitch)
        assert 'G:3' == str(b_notes[2].diatonic_pitch)
        assert 'A:3' == str(b_notes[3].diatonic_pitch)
        assert 'B:4' == str(b_notes[4].diatonic_pitch)

        s = '{C:4 [E:3 F [G:5 A B C] B]}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.sub_notes
        assert len(notes) == 2
        assert 'C:4' == str(notes[0].diatonic_pitch)
        assert isinstance(notes[1], Beam)
        beam = notes[1]
        b_notes = beam.sub_notes
        assert len(b_notes) == 4
        assert 'E:3' == str(b_notes[0].diatonic_pitch)
        assert 'F:3' == str(b_notes[1].diatonic_pitch)
        assert isinstance(b_notes[2], Beam)
        assert 'B:3' == str(b_notes[3].diatonic_pitch)
        bb_notes = b_notes[2].sub_notes
        assert len(bb_notes) == 4
        assert 'G:5' == str(bb_notes[0].diatonic_pitch)
        assert 'A:5' == str(bb_notes[1].diatonic_pitch)
        assert 'B:5' == str(bb_notes[2].diatonic_pitch)
        assert 'C:5' == str(bb_notes[3].diatonic_pitch)

    def test_tuplet(self):
        print('----- test_tuplet -----')
        l = LineGrammarExecutor()

        s = '{qC:4 D:4 ((1:8), 2)[E:3 F G]}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.sub_notes
        assert len(notes) == 3
        assert 'C:4' == str(notes[0].diatonic_pitch)
        assert 'D:4' == str(notes[1].diatonic_pitch)
        assert isinstance(notes[2], Tuplet)
        tuplet = notes[2]
        t_notes = tuplet.sub_notes
        assert len(t_notes) == 3
        assert 'E:3' == str(t_notes[0].diatonic_pitch)
        assert 'F:3' == str(t_notes[1].diatonic_pitch)
        assert 'G:3' == str(t_notes[2].diatonic_pitch)
        assert Duration(1, 4) == tuplet.duration
        assert Duration(1, 12) == t_notes[0].duration

        s = '{C:4 (q, 3)[E:3 F (i, 2)[G:5 A B] B]}'
        line, _ = l.parse(s)
        print(line)
        print('-----')

        notes = line.sub_notes
        assert len(notes) == 2
        assert 'C:4' == str(notes[0].diatonic_pitch)
        assert isinstance(notes[1], Tuplet)
        tuplet = notes[1]
        t_notes = tuplet.sub_notes
        assert len(t_notes) == 4
        assert 'E:3' == str(t_notes[0].diatonic_pitch)
        assert 'F:3' == str(t_notes[1].diatonic_pitch)
        assert isinstance(t_notes[2], Tuplet)
        assert 'B:3' == str(t_notes[3].diatonic_pitch)
        assert Duration(3, 4) == tuplet.duration

        assert isinstance(t_notes[2], Tuplet)
        tt_notes = t_notes[2].sub_notes
        assert len(tt_notes) == 3
        assert 'G:5' == str(tt_notes[0].diatonic_pitch)
        assert 'A:5' == str(tt_notes[1].diatonic_pitch)
        assert 'B:5' == str(tt_notes[2].diatonic_pitch)
        assert Duration(3, 16) == t_notes[2].duration

    def test_default_hct(self):
        print('----- test_default_hct -----')
        l = LineGrammarExecutor()

        s = '{qC:4 D:4 F}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 1
        hc = hclist[0]
        assert 'C-Major' == str(hc.tonality)
        assert ['C', 'E', 'G'] == [t[0].diatonic_symbol for t in hc.chord.tones]

    def test_simple_hct(self):
        print('----- test_simple_hct -----')
        l = LineGrammarExecutor()

        s = '{<Bb-Minor: ii>qC:4 D:4 <Cb-Major: IV> F G A}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 2
        first = hclist[0]
        second = hclist[1]
        assert 'Bb-MelodicMinor' == str(first.tonality)
        assert ['C', 'Eb', 'G'] == [t[0].diatonic_symbol for t in first.chord.tones]
        assert 'Cb-Major' == str(second.tonality)
        assert ['Fb', 'Ab', 'Cb'] == [t[0].diatonic_symbol for t in second.chord.tones]

        assert Duration(1,2) == first.duration
        assert Duration(3, 4) == second.duration

    def test_embedded_harmonic_tag(self):
        print('----- embedded_harmonic_tag -----')

        l = LineGrammarExecutor()

        s = '{qC:4 D:4 [<E-Major: IV> F G A]}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 2
        first = hclist[0]
        second = hclist[1]
        assert 'C-Major' == str(first.tonality)
        assert ['C', 'E', 'G'] == [t[0].diatonic_symbol for t in first.chord.tones]
        assert 'E-Major' == str(second.tonality)
        assert ['A', 'C#', 'E'] == [t[0].diatonic_symbol for t in second.chord.tones]

        assert Duration(1,2) == first.duration
        assert Duration(3, 8) == second.duration

        s = '{qC:4 D:4 <E-Major: IV> [F G A]}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 2
        first = hclist[0]
        second = hclist[1]
        assert 'C-Major' == str(first.tonality)
        assert ['C', 'E', 'G'] == [t[0].diatonic_symbol for t in first.chord.tones]
        assert 'E-Major' == str(second.tonality)
        assert ['A', 'C#', 'E'] == [t[0].diatonic_symbol for t in second.chord.tones]

        assert Duration(1,2) == first.duration
        assert Duration(3, 8) == second.duration

    def test_entangled_harmonic_tag(self):
        l = LineGrammarExecutor()

        s = '{qC:4 D:4 [E:3 <F-Major: IV> F A C]}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 2
        first = hclist[0]
        second = hclist[1]
        assert 'C-Major' == str(first.tonality)
        assert ['C', 'E', 'G'] == [t[0].diatonic_symbol for t in first.chord.tones]
        assert 'F-Major' == str(second.tonality)
        assert ['Bb', 'D', 'F'] == [t[0].diatonic_symbol for t in second.chord.tones]

        assert Duration(5, 8) == first.duration
        assert Duration(3, 8) == second.duration

        s = '{qC:4 D:4 (q, 3)[E:3 <F-Major: IV> F A C]}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 2
        first = hclist[0]
        second = hclist[1]
        assert 'C-Major' == str(first.tonality)
        assert ['C', 'E', 'G'] == [t[0].diatonic_symbol for t in first.chord.tones]
        assert 'F-Major' == str(second.tonality)
        assert ['Bb', 'D', 'F'] == [t[0].diatonic_symbol for t in second.chord.tones]

        assert Duration(11, 16) == first.duration
        assert Duration(9, 16) == second.duration

    def test_secondary_chord(self):
        print('----- test_secondary_chord -----')
        l = LineGrammarExecutor()

        s = '{<C-Major: V/V> F#:4 A D}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 1
        first = hclist[0]

        assert 'C-Major' == str(first.tonality)
        assert isinstance(first.chord.chord_template, SecondaryChordTemplate)
        assert 5 == first.chord.chord_template.secondary_scale_degree
        assert 5 == first.chord.chord_template.principal_chord_template.scale_degree

        s = '{<F-Major: IIIDom7/V-Natural> F#:4 A D}'
        line, hct = l.parse(s)
        print(line)
        print('-----')

        hclist = hct.hc_list()
        assert hclist is not None
        assert len(hclist) == 1
        first = hclist[0]

        assert 'F-Major' == str(first.tonality)
        assert isinstance(first.chord.chord_template, SecondaryChordTemplate)
        assert 5 == first.chord.chord_template.secondary_scale_degree
        assert 3 == first.chord.chord_template.principal_chord_template.scale_degree
        assert isinstance(first.chord.chord_template.principal_chord_template, TertianChordTemplate)
        assert TertianChordType(TertianChordType.Dom7) == first.chord.chord_template.principal_chord_template.chord_type
        assert 'C-NaturalMinor' == str(first.chord.secondary_tonality)
        assert {'Eb', 'G', 'Bb', 'Db'} == {t[0].diatonic_symbol for t in first.chord.tones}



