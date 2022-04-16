import unittest

from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from transformation.reflection.t_diatonic_reflection import TDiatonicReflection
from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.secondary_chord_template import SecondaryChordTemplate
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from tonalmodel.tonality import Tonality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_pitch import DiatonicPitch
from structure.note import Note
from structure.line import Line
from misc.interval import Interval
from timemodel.position import Position
from timemodel.duration import Duration
from harmonicmodel.tertian_chord_template import TertianChordType
from fractions import Fraction

import logging


class TestTFlip(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hct_rebuild_perfect_overlap(self):
        print('----- test_hct_rebuild_perfect_overlap -----')

        line_str = '{<C-Major: I> hA:5 <:IV> B  qC G <:VI> hD}'
        lge = LineGrammarExecutor()
        target_line, target_hct = lge.parse(line_str)
        TestTFlip.print_hct(target_hct)

        cue = DiatonicPitch(5, 'd')

        tflip = TDiatonicReflection(target_line, target_hct, cue)

        temporal_extent = Interval(Fraction(1, 2), Fraction(3, 2))
        score_line, score_hct = tflip.apply(temporal_extent, cue)
        TestTFlip.print_notes(score_line)
        TestTFlip.print_hct(score_hct)

        hc_list = score_hct.hc_list()
        assert hc_list[0].position == Position(0)
        assert hc_list[0].duration == Duration(1, 2)
        assert hc_list[0].chord.chord_type == TertianChordType(TertianChordType.Maj)
        assert hc_list[0].chord.chord_template.scale_degree == 1
        assert {t[0].diatonic_symbol for t in hc_list[0].chord.tones} == {'C', 'E', 'G'}
        assert hc_list[0].chord.chord_template.inversion == 1

        assert hc_list[1].position == Position(1, 2)
        assert hc_list[1].duration == Duration(1)
        assert hc_list[1].chord.chord_type == TertianChordType(TertianChordType.Min)
        assert hc_list[1].chord.chord_template.scale_degree == 3
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'G', 'B', 'E'}
        assert hc_list[1].chord.chord_template.inversion == 3

        assert hc_list[2].position == Position(3, 2)
        assert hc_list[2].duration == Duration(1, 2)
        assert hc_list[2].chord.chord_type == TertianChordType(TertianChordType.Min)
        assert hc_list[2].chord.chord_template.scale_degree == 6
        assert {t[0].diatonic_symbol for t in hc_list[2].chord.tones} == {'A', 'C', 'E'}
        assert hc_list[2].chord.chord_template.inversion == 1

        notes = score_line.get_all_notes()
        assert str(notes[1].diatonic_pitch) == "F:4"
        assert str(notes[2].diatonic_pitch) == "E:5"
        assert str(notes[3].diatonic_pitch) == "A:4"

    def test_hct_rebuild_imperfect_overlap(self):
        print('----- test_hct_rebuild_imperfect_overlap -----')
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("D"))
        chord_t_i = TertianChordTemplate.parse('tI')
        chord_i = chord_t_i.create_chord(diatonic_tonality)

        chord_t_iv = TertianChordTemplate.parse('tIV')
        chord_iv = chord_t_iv.create_chord(diatonic_tonality)

        chord_t_v = TertianChordTemplate.parse('tV')
        chord_v = chord_t_v.create_chord(diatonic_tonality)

        chord_t_vi = TertianChordTemplate.parse('tVI')
        chord_vi = chord_t_vi.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord_i, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_iv, Duration(1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_v, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_vi, Duration(1)))
        TestTFlip.print_hct(hc_track)

        line_str = '{<D-Major: I> hA:5 <:IV> B  C# <:V> qD E <:VI> hF# qG A}'
        lge = LineGrammarExecutor()
        target_line, target_hct = lge.parse(line_str)
        TestTFlip.print_hct(target_hct)

        cue = DiatonicPitch(5, 'f#')

        tflip = TDiatonicReflection(target_line, target_hct, cue)

        temporal_extent = Interval(Fraction(1, 4), Fraction(9, 4))
        score_line, score_hct = tflip.apply(temporal_extent, cue)
        TestTFlip.print_notes(score_line)
        TestTFlip.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert len(notes) == 8
        assert str(notes[0].diatonic_pitch) == 'A:5'
        assert str(notes[1].diatonic_pitch) == 'C#:5'
        assert str(notes[2].diatonic_pitch) == 'B:5'
        assert str(notes[3].diatonic_pitch) == 'A:5'
        assert str(notes[4].diatonic_pitch) == 'G:5'
        assert str(notes[5].diatonic_pitch) == 'F#:5'
        assert str(notes[6].diatonic_pitch) == 'G:5'
        assert str(notes[7].diatonic_pitch) == 'A:5'

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 6
        assert hc_list[0].chord.chord_template.scale_degree == 1
        assert {t[0].diatonic_symbol for t in hc_list[0].chord.tones} == {'D', 'F#', 'A'}
        assert hc_list[0].chord.chord_template.inversion == 1

        assert hc_list[1].chord.chord_template.scale_degree == 1
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'D', 'F#', 'A'}
        assert hc_list[1].chord.chord_template.inversion == 3

        assert hc_list[2].chord.chord_template.scale_degree == 5
        assert {t[0].diatonic_symbol for t in hc_list[2].chord.tones} == {'E', 'A', 'C#'}
        assert hc_list[2].chord.chord_template.inversion == 3

        assert hc_list[3].chord.chord_template.scale_degree == 4
        assert {t[0].diatonic_symbol for t in hc_list[3].chord.tones} == {'D', 'G', 'B'}
        assert hc_list[3].chord.chord_template.inversion == 3

        assert hc_list[4].chord.chord_template.scale_degree == 3
        assert {t[0].diatonic_symbol for t in hc_list[4].chord.tones} == {'C#', 'F#', 'A'}
        assert hc_list[4].chord.chord_template.inversion == 3

        assert hc_list[5].chord.chord_template.scale_degree == 6
        assert {t[0].diatonic_symbol for t in hc_list[5].chord.tones} == {'B', 'D', 'F#'}
        assert hc_list[5].chord.chord_template.inversion == 1

    def test_mozart(self):
        print('----- Mozart -----')
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chort_t_i = TertianChordTemplate.parse('tI')
        chord_i = chort_t_i.create_chord(diatonic_tonality)

        chort_t_v = TertianChordTemplate.parse('tVMaj7')
        chord_v = chort_t_v.create_chord(diatonic_tonality)

        chord_t_i_1 = TertianChordTemplate.parse('tI')
        chord_i_1 = chord_t_i_1.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord_i, Duration(1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_v, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_i_1, Duration(1, 2)))
        TestTFlip.print_hct(hc_track)

        tune = [('C:5', (1, 2)), ('E:5', (1, 4)), ('G:5', (1, 4)), ('B:4', (3, 8)), ('C:5', (1, 16)),
                ('D:5', (1, 16)), ('C:5', (1, 4))]
        line = TestTFlip.build_line(tune)

        cue = DiatonicPitch(5, 'd')

        tflip = TDiatonicReflection(line, hc_track, cue)

        temporal_extent = Interval(Fraction(0), Fraction(2))
        score_line, score_hct = tflip.apply(temporal_extent, cue)
        TestTFlip.print_notes(score_line)
        TestTFlip.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert len(notes) == 7
        assert str(notes[0].diatonic_pitch) == 'E:5'
        assert str(notes[1].diatonic_pitch) == 'C:5'
        assert str(notes[2].diatonic_pitch) == 'A:4'
        assert str(notes[3].diatonic_pitch) == 'F:5'
        assert str(notes[4].diatonic_pitch) == 'E:5'
        assert str(notes[5].diatonic_pitch) == 'D:5'
        assert str(notes[6].diatonic_pitch) == 'E:5'

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 3
        assert hc_list[0].chord.chord_template.scale_degree == 6
        assert {t[0].diatonic_symbol for t in hc_list[0].chord.tones} == {'E', 'A', 'C'}
        assert hc_list[0].chord.chord_template.inversion == 3

        assert hc_list[1].chord.chord_template.scale_degree == 2
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'A', 'D', 'F', 'Bb'}
        assert hc_list[1].chord.chord_template.inversion == 3

        assert hc_list[2].chord.chord_template.scale_degree == 6
        assert {t[0].diatonic_symbol for t in hc_list[2].chord.tones} == {'E', 'A', 'C'}
        assert hc_list[2].chord.chord_template.inversion == 3

    def test_secondary_chord(self):
        print('----- test_secondary_tonality -----')
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chort_t_i = TertianChordTemplate.parse('tI')
        chord_i = chort_t_i.create_chord(diatonic_tonality)

        chord_v_ii = SecondaryChordTemplate.parse('V/ii').create_chord(diatonic_tonality)
        chord_vi_v = SecondaryChordTemplate.parse('vi/V').create_chord(diatonic_tonality)

        chord_t_ii = TertianChordTemplate.parse('tii')
        chord_ii = chord_t_ii.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord_i, Duration(1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_v_ii, Duration(1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_vi_v, Duration(1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_ii, Duration(1)))
        TestTFlip.print_hct(hc_track)

        tune = [('C:5', (1, 1)), ('E:5', (1, 1)), ('E:5', (1, 1)), ('G:5', (1, 1))]
        line = TestTFlip.build_line(tune)

        cue = DiatonicPitch(5, 'd')

        tflip = TDiatonicReflection(line, hc_track, cue)

        temporal_extent = Interval(Fraction(0), Fraction(4))
        score_line, score_hct = tflip.apply(temporal_extent, cue)
        TestTFlip.print_notes(score_line)
        TestTFlip.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert len(notes) == 4
        assert str(notes[0].diatonic_pitch) == 'E:5'
        assert str(notes[1].diatonic_pitch) == 'C#:5'
        assert str(notes[2].diatonic_pitch) == 'C:5'
        assert str(notes[3].diatonic_pitch) == 'A:4'

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 4
        assert hc_list[1].chord.primary_chord.chord_template.scale_degree == 7
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'C#', 'E', 'G'}
        assert hc_list[1].chord.primary_chord.chord_template.inversion == 3

        assert hc_list[2].chord.primary_chord.chord_template.scale_degree == 7
        assert {t[0].diatonic_symbol for t in hc_list[2].chord.tones} == {'C', 'F#', 'A'}
        assert hc_list[2].chord.primary_chord.chord_template.inversion == 3

    def test_secondary_tonality_2(self):
        print('----- test_secondary_tonality 2 -----')
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chort_t_i = TertianChordTemplate.parse('tI')
        chord_i = chort_t_i.create_chord(diatonic_tonality)

        chord_vi_v = SecondaryChordTemplate.parse('vi/V').create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord_i, Duration(1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord_vi_v, Duration(1)))
        TestTFlip.print_hct(hc_track)

        tune = [('C:5', (1, 1)), ('E:5', (1, 1))]
        line = TestTFlip.build_line(tune)

        cue = DiatonicPitch(5, 'f')

        tflip = TDiatonicReflection(line, hc_track, cue)

        temporal_extent = Interval(Fraction(0), Fraction(2))
        score_line, score_hct = tflip.apply(temporal_extent, cue)
        TestTFlip.print_notes(score_line)
        TestTFlip.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert len(notes) == 2
        assert str(notes[0].diatonic_pitch) == 'B:5'
        assert str(notes[1].diatonic_pitch) == 'F#:5'

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 2
        assert hc_list[1].chord.primary_chord.chord_template.scale_degree == 3
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'F#', 'B', 'D'}
        assert hc_list[1].chord.primary_chord.chord_template.inversion == 3

    @staticmethod
    def build_line(note_spec_list):
        note_list = list()
        for spec in note_spec_list:
            pitch = DiatonicPitch.parse(spec[0])
            n = Note(pitch, Duration(spec[1][0], spec[1][1]))
            note_list.append(n)
        return Line(note_list)

    @staticmethod
    def print_hct(hct):
        hcs = hct.hc_list()
        index = 0
        for hc in hcs:
            print('[{0}] {1} {2}'.format(index, hc, hc.position))
            index += 1
        print("--------")

    @staticmethod
    def print_notes(line):
        for note in line.get_all_notes():
            print(note)
        print("--------")
