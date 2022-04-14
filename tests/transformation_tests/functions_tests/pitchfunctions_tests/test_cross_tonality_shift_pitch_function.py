import logging
import sys
import unittest

from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.interval import IntervalType, Interval
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.tonality import Tonality
from transformation.functions.pitchfunctions.cross_tonality_shift_pitch_function import \
    CrossTonalityShiftPitchFunction


class TestCrossTonalityShiftPitchFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_diatonic_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))
        i = Interval(5, IntervalType.Perfect)
        r = PitchRange.create('E:3', 'E:7')

        f = CrossTonalityShiftPitchFunction(t_domain, r, i)

        print('f={0}'.format(f))

        TestCrossTonalityShiftPitchFunction.print_map('test_diatonic_function', f)

        t = f.tonal_function
        print(t)

        assert 'P:5' == str(f.root_shift_interval)

        assert 'G' == t['C'].diatonic_symbol
        assert 'A' == t['D'].diatonic_symbol
        assert 'B' == t['E'].diatonic_symbol
        assert 'C' == t['F'].diatonic_symbol
        assert 'D' == t['G'].diatonic_symbol
        assert 'E' == t['A'].diatonic_symbol
        assert 'F#' == t['B'].diatonic_symbol

        # test diatonic maps
        assert 'G:5' == str(f['C:5'])
        assert 'F#:5' == str(f['B:4'])
        assert 'E:5' == str(f['A:4'])
        assert 'D:5' == str(f['G:4'])
        assert 'C:5' == str(f['F:4'])
        assert 'B:4' == str(f['E:4'])
        assert 'A:4' == str(f['D:4'])
        assert 'G:4' == str(f['C:4'])

        # test range
        d = f.domain_pitch_range
        print(d)
        assert d.start_index == DiatonicPitch.parse('E:3').chromatic_distance
        assert d.end_index == DiatonicPitch.parse('E:7').chromatic_distance
        r = f.range_pitch_range
        print(r)
        assert r.start_index == DiatonicPitch.parse('B:3').chromatic_distance
        assert r.end_index == DiatonicPitch.parse('B:7').chromatic_distance

        # test chromatics
        assert 'G#:5' == str(f['C#:5'])
        assert 'F##:5' == str(f['B#:4'])
        assert 'E#:5' == str(f['A#:4'])
        assert 'D#:5' == str(f['G#:4'])
        assert 'C#:5' == str(f['F#:4'])
        assert 'B#:4' == str(f['E#:4'])
        assert 'A#:4' == str(f['D#:4'])
        assert 'G#:4' == str(f['C#:4'])

        assert 'Gb:5' == str(f['Cb:5'])
        assert 'F:5' == str(f['Bb:4'])
        assert 'Eb:5' == str(f['Ab:4'])
        assert 'Db:5' == str(f['Gb:4'])
        assert 'Cb:5' == str(f['Fb:4'])
        assert 'Bb:4' == str(f['Eb:4'])
        assert 'Ab:4' == str(f['Db:4'])
        assert 'Gb:4' == str(f['Cb:4'])

        TestCrossTonalityShiftPitchFunction.print_book_map('test_diatonic_function', f)

    def test_pentatonic_tonal_function(self):
        t_domain = Tonality.create(ModalityType.MinorPentatonic, DiatonicTone('C'))
        i = Interval(5, IntervalType.Perfect)
        r = PitchRange.create('E:3', 'E:7')

        f = CrossTonalityShiftPitchFunction(t_domain, r, i)

        print('f={0}'.format(f))

        TestCrossTonalityShiftPitchFunction.print_map('test_pentatonic_tonal_function', f)

        t = f.tonal_function
        print(t)

        assert 'G' == t['C'].diatonic_symbol
        assert 'Bb' == t['Eb'].diatonic_symbol
        assert 'C' == t['F'].diatonic_symbol
        assert 'D' == t['G'].diatonic_symbol
        assert 'F' == t['Bb'].diatonic_symbol

        assert 'G:5' == str(f['C:5'])
        assert 'F:5' == str(f['Bb:4'])
        assert 'D:5' == str(f['G:4'])
        assert 'C:5' == str(f['F:4'])
        assert 'Bb:4' == str(f['Eb:4'])
        assert 'G:4' == str(f['C:4'])

        # test range
        d = f.domain_pitch_range
        print(d)
        assert d.start_index == DiatonicPitch.parse('E:3').chromatic_distance
        assert d.end_index == DiatonicPitch.parse('E:7').chromatic_distance
        r = f.range_pitch_range
        print(r)
        assert r.start_index == DiatonicPitch.parse('B:3').chromatic_distance
        assert r.end_index == DiatonicPitch.parse('B:7').chromatic_distance

        # test chromatics
        assert 'G#:5' == str(f['C#:5'])
        assert 'F#:5' == str(f['B:4'])
        assert 'E#:5' == str(f['A#:4'])
        assert 'E:5' == str(f['A:4'])
        assert 'D#:5' == str(f['G#:4'])
        assert 'C#:5' == str(f['F#:4'])
        assert 'B:4' == str(f['E:4'])
        assert 'A:4' == str(f['D:4'])
        assert 'A#:4' == str(f['D#:4'])
        assert 'G#:4' == str(f['C#:4'])

        assert 'Gb:5' == str(f['Cb:5'])
        assert 'Fb:5' == str(f['Bbb:4'])
        assert 'Eb:5' == str(f['Ab:4'])
        assert 'Db:5' == str(f['Gb:4'])
        assert 'Cb:5' == str(f['Fb:4'])
        assert 'Bbb:4' == str(f['Ebb:4'])
        assert 'Ab:4' == str(f['Db:4'])
        assert 'Gb:4' == str(f['Cb:4'])

    def test_diatonic_modal_indexed_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))
        i = Interval(2, IntervalType.Major)
        r = PitchRange.create('E:3', 'E:7')

        f = CrossTonalityShiftPitchFunction(t_domain, r, i, modal_index=4)

        print('f={0}'.format(f))

        TestCrossTonalityShiftPitchFunction.print_map('test_diatonic_function', f)

        t = f.tonal_function
        print(t)

        # test diatonic maps
        assert 'D:4' == str(f['C:4'])
        assert 'E:4' == str(f['D:4'])
        assert 'F#:4' == str(f['E:4'])
        assert 'G:4' == str(f['F:4'])
        assert 'A:4' == str(f['G:4'])
        assert 'B:4' == str(f['A:4'])
        assert 'C:5' == str(f['B:4'])
        assert 'D:5' == str(f['C:5'])

        assert 'M:2' == str(f.root_shift_interval)

    def test_shift_create(self):
        t_domain = Tonality.create(ModalityType.MelodicMinor, DiatonicTone('C'))
        i = Interval(5, IntervalType.Perfect)
        r = PitchRange.create('E:3', 'E:7')

        f = CrossTonalityShiftPitchFunction(t_domain, r, i)

        assert 'P:5' == str(f.root_shift_interval)

        assert 'G:4' == str(f['C:4'])
        assert 'A:4' == str(f['D:4'])
        assert 'B:4' == str(f['E:4'])
        assert 'C:5' == str(f['F:4'])

    def test_additional_octaves(self):
        t_domain = Tonality.create(ModalityType.MinorPentatonic, DiatonicTone('C'))
        i = Interval(12, IntervalType.Perfect)
        r = PitchRange.create('E:3', 'E:7')

        f = CrossTonalityShiftPitchFunction(t_domain, r, i)

        print('f={0}'.format(f))

        assert 'P:12' == str(f.root_shift_interval)

        assert 'G:5' == str(f['C:4'])
        assert 'A:5' == str(f['D:4'])
        assert 'B:5' == str(f['E:4'])
        assert 'C:6' == str(f['F:4'])

        i = Interval(11, IntervalType.Perfect).negation()
        f = CrossTonalityShiftPitchFunction(t_domain, r, i)
        print('f={0}'.format(f))

        assert '-P:11' == str(f.root_shift_interval)

        assert 'G:2' == str(f['C:4'])
        assert 'A:2' == str(f['D:4'])
        assert 'B:2' == str(f['E:4'])
        assert 'C:3' == str(f['F:4'])

    @staticmethod
    def print_map(tag, fctn):
        print(tag)
        keys = sorted([i for i in fctn.map.keys()])
        for key in keys:
            print('{0} --> {1}'.format(key, fctn[key]))

    @staticmethod
    def print_book_map(tag, f):
        print(tag)
        domain_tonality = f.domain_tonality
        range_tonality = f.range_tonality

        print('CrossTonalityShiftPitchFunction {0}--> {1}'.format(domain_tonality, range_tonality))

        domain_annotation = domain_tonality.annotation[:-1]
        presentation_reg = 4
        domain_presentation_pitches = list()
        last_pitch = None
        for t in domain_annotation:
            domain_pitch = DiatonicPitch(presentation_reg, t)
            # augment register if crossing past C, e.g. B:4 > C:4
            if last_pitch is not None and last_pitch.chromatic_distance > domain_pitch.chromatic_distance:
                presentation_reg = presentation_reg + 1
                domain_pitch = DiatonicPitch(presentation_reg, t)

            for a in [-1, 0, 1]:
                a_tone = DiatonicTone.alter_tone_by_augmentation(t, a)
                domain_pitch_mod = DiatonicPitch(presentation_reg, a_tone)
                domain_presentation_pitches.append(domain_pitch_mod)
            last_pitch = domain_pitch

        for domain_pitch in domain_presentation_pitches:
            range_pitch = f[domain_pitch]
            print('{0} --> {1}'.format(domain_pitch, range_pitch))
