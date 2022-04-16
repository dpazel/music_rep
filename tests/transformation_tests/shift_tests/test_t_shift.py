import unittest

from harmonicmodel.chord_template import ChordTemplate
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from tonalmodel.tonality import Tonality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_pitch import DiatonicPitch
from structure.note import Note
from structure.line import Line
from misc.interval import Interval
from timemodel.duration import Duration
from harmonicmodel.tertian_chord_template import TertianChordType
from fractions import Fraction

from tonalmodel.interval import Interval as TonalInterval

import logging

from transformation.shift.t_shift import TShift


class TestTShift(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hct_simple_shift(self):
        print('----- test_hct_simple_shift -----')

        line_str = '{<C-Major: I> C:4 E F D <:IV> F A <:V> G D <:VI> a c b a}'
        lge = LineGrammarExecutor()
        target_line, target_hct = lge.parse(line_str)

        root_shift_interval = TonalInterval.create_interval('C:4', 'G:4')

        tshift = TShift(target_line, target_hct, root_shift_interval)

        temporal_extent = Interval(Fraction(1, 1), Fraction(2, 1))
        tshift.apply(temporal_extent, as_copy=False)
        TestTShift.print_notes(target_line)
        TestTShift.print_hct(target_hct)

        notes = target_line.get_all_notes()
        assert 12 == len(notes)
        assert 'C:5' == str(notes[4].diatonic_pitch)
        assert 'E:5' == str(notes[5].diatonic_pitch)
        assert 'D:5' == str(notes[6].diatonic_pitch)
        assert 'A:4' == str(notes[7].diatonic_pitch)

        hc_list = target_hct.hc_list()
        assert len(hc_list) == 4
        assert hc_list[1].chord.chord_template.scale_degree == 4
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'C', 'E', 'G'}
        assert hc_list[1].chord.chord_template.inversion == 1
        assert hc_list[1].tonality.modal_index == 0
        assert hc_list[1].tonality.basis_tone.diatonic_symbol == 'G'
        assert hc_list[1].tonality.root_tone.diatonic_symbol == 'G'
        assert hc_list[1].tonality.modality_type == ModalityType.Major
        assert hc_list[1].chord.chord_type.value == TertianChordType.Maj

    def test_modal_setting(self):
        print('----- test_modal_setting -----')

        line_str = '{<C-Major: I> C:4 E G A <:IV> iF A B C:5 <:V> qG:4 D <:VI> a c:5 b:4 a}'
        lge = LineGrammarExecutor()
        target_line, target_hct = lge.parse(line_str)

        root_shift_interval = TonalInterval.create_interval('C:4', 'C#:4')

        tshift = TShift(target_line, target_hct, root_shift_interval, default_modal_index=2)

        temporal_extent = Interval(Fraction(0), Fraction(3, 1))
        score_line, score_hct = tshift.apply(temporal_extent)

        TestTShift.print_notes(score_line)
        TestTShift.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert 14 == len(notes)
        assert 'F#:4' == str(notes[4].diatonic_pitch)
        assert 'A:4' == str(notes[5].diatonic_pitch)
        assert 'B:4' == str(notes[6].diatonic_pitch)
        assert 'C#:5' == str(notes[7].diatonic_pitch)

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 4
        assert hc_list[0].chord.chord_template.scale_degree == 1
        assert {t[0].diatonic_symbol for t in hc_list[0].chord.tones} == {'C#', 'E', 'G#'}
        assert hc_list[0].chord.chord_template.inversion == 1
        assert hc_list[0].tonality.modal_index == 2
        assert hc_list[0].tonality.basis_tone.diatonic_symbol == 'A'
        assert hc_list[0].tonality.root_tone.diatonic_symbol == 'C#'
        assert hc_list[0].tonality.modality_type == ModalityType.Major
        assert hc_list[0].chord.chord_type.value == TertianChordType.Min

    def test_modality_setting(self):
        print('----- test_modality_setting -----')

        line_str = '{<C-Major: I> C:4 E G A <:IV> iF A B C:5 <:V> qG:4 D <:VI> a c:5 b:4 a}'
        lge = LineGrammarExecutor()
        target_line, target_hct = lge.parse(line_str)

        root_shift_interval = TonalInterval.create_interval('C:4', 'C#:4')

        tshift = TShift(target_line, target_hct, root_shift_interval, default_modal_index=2)

        temporal_extent = Interval(Fraction(0), Fraction(3, 1))
        score_line, score_hct = tshift.apply(temporal_extent, range_modality_type=ModalityType.MelodicMinor)

        TestTShift.print_notes(score_line)
        TestTShift.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert 14 == len(notes)
        assert 'F##:4' == str(notes[4].diatonic_pitch)
        assert 'A#:4' == str(notes[5].diatonic_pitch)
        assert 'B#:4' == str(notes[6].diatonic_pitch)
        assert 'C#:5' == str(notes[7].diatonic_pitch)

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 4
        assert hc_list[0].chord.chord_template.scale_degree == 1
        assert {t[0].diatonic_symbol for t in hc_list[0].chord.tones} == {'C#', 'E#', 'G##'}
        assert hc_list[0].chord.chord_template.inversion == 1
        assert hc_list[0].tonality.modal_index == 2
        assert hc_list[0].tonality.basis_tone.diatonic_symbol == 'A#'
        assert hc_list[0].tonality.root_tone.diatonic_symbol == 'C#'
        assert hc_list[0].tonality.modality_type == ModalityType.MelodicMinor
        assert hc_list[0].chord.chord_type.value == TertianChordType.Aug

    def test_modal_tonality_modal_index(self):
        print('----- test_modal_tonality_modal_index -----')
        # diatonic_modality is effectively Dorian

        line_str = '{<D-Major(1): I> D:4 F A B <:IV> iG B C:5 D <:V> qA:4 E <:VI> qB D:5 C B}'
        lge = LineGrammarExecutor()
        target_line, target_hct = lge.parse(line_str)

        # shift whole score sot D being Phrygian in some major scale - scale being Bb-Major
        tshift = TShift(target_line, target_hct, default_root_shift_interval=None, default_modal_index=2)

        temporal_extent = Interval(Fraction(0), Fraction(3, 1))
        score_line, score_hct = tshift.apply(temporal_extent)

        TestTShift.print_notes(score_line)
        TestTShift.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert 14 == len(notes)
        assert 'G:4' == str(notes[4].diatonic_pitch)
        assert 'B:4' == str(notes[5].diatonic_pitch)
        assert 'Cb:5' == str(notes[6].diatonic_pitch)
        assert 'D:5' == str(notes[7].diatonic_pitch)

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 4
        assert hc_list[0].chord.chord_template.scale_degree == 1
        assert {t[0].diatonic_symbol for t in hc_list[0].chord.tones} == {'E', 'G', 'B'}
        assert hc_list[0].chord.chord_template.inversion == 1
        assert hc_list[0].tonality.modal_index == 2
        assert hc_list[0].tonality.basis_tone.diatonic_symbol == 'C'
        assert hc_list[0].tonality.root_tone.diatonic_symbol == 'E'
        assert hc_list[0].tonality.modality_type == ModalityType.Major
        assert hc_list[0].chord.chord_type.value == TertianChordType.Min

    def test_modal_secondary_tonality(self):
        print('----- test_modal_tonality_modal_index -----')
        # diatonic_modality is effectively Dorian
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone('C'))

        chords = [('tI', 1), ('V/iii', (1, 2)), ('tiii', (1, 2)), ('tVI', 1)]
        hc_track = TestTShift.create_track(chords, diatonic_tonality)
        TestTShift.print_hct(hc_track)

        s_notes = [
            ('C:4', 'q'),
            ('E:4', 'q'),
            ('G:4', 'q'),
            ('A:4', 'q'),

            ('B:4', 'e'),
            ('C#5', 'e'),
            ('d#:5', 'e'),
            ('e:5', 'e'),

            ('b:4', 'q'),
            ('g:4', 'q'),

            ('a:4', 'q'),
            ('c:5', (1, 4)),
            ('b:5', (1, 4)),
            ('a:4', (1, 4)),
        ]

        line = TestTShift.create_line(s_notes)
        root_shift_interval = TonalInterval.create_interval('C:4', 'F:4')

        tshift = TShift(line, hc_track, root_shift_interval, default_range_modality_type=ModalityType.MelodicMinor)

        temporal_extent = Interval(Fraction(0), Fraction(3, 1))
        score_line, score_hct = tshift.apply(temporal_extent, range_modality_type=ModalityType.MelodicMinor,
                                             as_copy=False)

        TestTShift.print_notes(score_line)
        TestTShift.print_hct(score_hct)

        notes = score_line.get_all_notes()
        assert 14 == len(notes)
        assert 'Eb:5' == str(notes[4].diatonic_pitch)
        assert 'F:5' == str(notes[5].diatonic_pitch)
        assert 'G:5' == str(notes[6].diatonic_pitch)
        assert 'Ab:5' == str(notes[7].diatonic_pitch)

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 4
        assert hc_list[1].chord.chord_template.secondary_scale_degree == 3
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'Eb', 'G', 'Bb'}
        assert hc_list[1].chord.chord_template.principal_chord_template.inversion == 1
        assert hc_list[1].tonality.modal_index == 0
        assert hc_list[1].tonality.basis_tone.diatonic_symbol == 'F'
        assert hc_list[1].tonality.root_tone.diatonic_symbol == 'F'
        assert hc_list[1].tonality.modality_type == ModalityType.MelodicMinor
        assert hc_list[1].chord.chord_type.value == TertianChordType.Maj

    @staticmethod
    def create_track(chords, tonality):
        hc_track = HarmonicContextTrack()
        for c in chords:
            chord_t = ChordTemplate.generic_chord_template_parse(c[0])
            chord = chord_t.create_chord(tonality)
            duration = Duration(c[1]) if isinstance(c[1], int) else Duration(c[1][0], c[1][1])
            hc_track.append(HarmonicContext(tonality, chord, duration))
        return hc_track

    @staticmethod
    def create_line(note_spec_list):
        note_list = list()
        for spec in note_spec_list:
            pitch = DiatonicPitch.parse(spec[0])
            if isinstance(spec[1], str):
                s_d = spec[1].upper()
                if s_d == 'Q':
                    d = Duration(1, 4)
                elif s_d == 'H':
                    d = Duration(1, 2)
                elif s_d == 'W':
                    d = Duration(1)
                elif s_d == 'E':
                    d = Duration(1, 8)
                elif s_d == 'S':
                    d = Duration(1, 16)
                else:
                    d = Duration(1, 4)
            else:
                d = Duration(spec[1][0], spec[1][1])
            n = Note(pitch, d)
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
