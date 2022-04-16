import unittest

import logging

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.secondary_chord_template import SecondaryChordTemplate
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.line import Line
from structure.note import Note
from timemodel.duration import Duration
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from transformation.reflection.t_chromatic_reflection import TChromaticReflection
from misc.interval import Interval
from tonalmodel.diatonic_pitch import DiatonicPitch

from fractions import Fraction


class TestTChromaticFlip(unittest.TestCase):
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

        print('--- before transformation ---')
        TestTChromaticFlip.print_notes(target_line)
        TestTChromaticFlip.print_hct(target_hct)

        cue = DiatonicPitch(5, 'c')

        f = TChromaticReflection(target_line, target_hct, cue)

        temporal_extent = Interval(Fraction(1, 2), Fraction(3, 2))
        score_line, score_hct = f.apply(temporal_extent, cue)
        print('--- after transformation ---')
        TestTChromaticFlip.print_notes(score_line)
        TestTChromaticFlip.print_hct(score_hct)

        print('--- transformation ---')
        TestTChromaticFlip.print_function(f, target_hct)

        notes = score_line.get_all_notes()
        assert 'Db:4' == str(notes[1].diatonic_pitch)
        assert 'C:5' == str(notes[2].diatonic_pitch)
        assert 'F:4' == str(notes[3].diatonic_pitch)

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 3
        assert hc_list[1].chord.chord_template.scale_degree == 1
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'G', 'C', 'Eb'}
        assert hc_list[1].chord.chord_template.inversion == 3

    def test_mozart(self):
        print('----- Mozart -----')

        line_str = '{<C-Major: I> hC:5 qE G <:VMaj7> q@b:4 sC:5 D <:I> hC}'
        lge = LineGrammarExecutor()
        target_line, target_hct = lge.parse(line_str)

        print('--- before transformation ---')
        TestTChromaticFlip.print_notes(target_line)
        TestTChromaticFlip.print_hct(target_hct)

        cue = DiatonicPitch(5, 'c')

        f = TChromaticReflection(target_line, target_hct, cue)
        score_line, score_hct = f.apply()
        print('--- after transformation ---')
        TestTChromaticFlip.print_notes(score_line)
        TestTChromaticFlip.print_hct(score_hct)

        print('--- transformation ---')
        TestTChromaticFlip.print_function(f, target_hct)

        notes = score_line.get_all_notes()
        assert 'C:5' == str(notes[0].diatonic_pitch)
        assert 'Ab:4' == str(notes[1].diatonic_pitch)
        assert 'F:4' == str(notes[2].diatonic_pitch)
        assert 'Db:5' == str(notes[3].diatonic_pitch)
        assert 'C:5' == str(notes[4].diatonic_pitch)
        assert 'Bb:4' == str(notes[5].diatonic_pitch)
        assert 'C:5' == str(notes[6].diatonic_pitch)

        hc_list = score_hct.hc_list()
        assert len(hc_list) == 3
        assert hc_list[0].chord.chord_template.scale_degree == 4
        assert {t[0].diatonic_symbol for t in hc_list[0].chord.tones} == {'C', 'F', 'Ab'}
        assert hc_list[0].chord.chord_template.inversion == 3

        assert hc_list[1].chord.chord_template.scale_degree == 7
        assert {t[0].diatonic_symbol for t in hc_list[1].chord.tones} == {'F', 'Bb', 'Db', 'Gb'}
        assert hc_list[1].chord.chord_template.inversion == 3

        assert hc_list[2].chord.chord_template.scale_degree == 4
        assert {t[0].diatonic_symbol for t in hc_list[2].chord.tones} == {'C', 'F', 'Ab'}
        assert hc_list[2].chord.chord_template.inversion == 3

    def test_secondary_chord(self):
        print('----- test_secondary_tonality -----')
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicFoundation.get_tone("C"))
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
        TestTChromaticFlip.print_hct(hc_track)

        tune = [('C:5', (1, 1)), ('E:5', (1, 1)), ('E:5', (1, 1)), ('G:5', (1, 1))]
        line = TestTChromaticFlip.build_line(tune)

        cue = DiatonicPitch(5, 'd')

        tflip = TChromaticReflection(line, hc_track, cue)

        score_line, score_hct = tflip.apply()
        TestTChromaticFlip.print_notes(score_line)
        TestTChromaticFlip.print_hct(score_hct)

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

    @staticmethod
    def print_map(f, source_hct):
        for hc in source_hct.hc_list():
            if hc in f.hc_flip_map:
                pitch_map = f.hc_flip_map[hc]
                map_list = list()
                for tone in pitch_map.domain_tonality.annotation[:-1]:
                    ft = pitch_map.tonal_function[tone]
                    map_list.append('{0}-->{1}'.format(tone.diatonic_symbol, ft.diatonic_symbol))
                print('[{0}] ({1})  {2}'.format(hc, pitch_map.range_tonality, ', '.join([s for s in map_list])))

    @staticmethod
    def print_function(f, source_hct):
        for hc in source_hct.hc_list():
            if hc in f.hc_flip_map:
                pitch_map = f.hc_flip_map[hc]

                domain = sorted([p for p in pitch_map.domain], key=lambda p: p.chromatic_distance)
                domain_tones = pitch_map.domain_tonality.annotation[:-1]
                map_list = list()
                for p in domain:
                    r = pitch_map[p]
                    if p.diatonic_tone in domain_tones:
                        map_list.append('{0} --> {1}'.format(p, r))

                print('[{0}] ({1}) {2}:  {3}'.format(pitch_map.domain_tonality,
                                                     pitch_map.cue_pitch,
                                                     pitch_map.range_tonality,
                                                     ', '.join([s for s in map_list])
                                                     )
                      )

    @staticmethod
    def build_line(note_spec_list):
        note_list = list()
        for spec in note_spec_list:
            pitch = DiatonicPitch.parse(spec[0])
            n = Note(pitch, Duration(spec[1][0], spec[1][1]))
            note_list.append(n)
        return Line(note_list)
