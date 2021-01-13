import logging
import sys
import unittest

from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.tonality import Tonality
from transformation.functions.pitchfunctions.diatonic_pitch_reflection_function import FlipType, DiatonicPitchReflectionFunction


class TestFlipOnTonality(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_centered_odd_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('E'))
        r = PitchRange.create('E:3', 'E:7')

        f = DiatonicPitchReflectionFunction(t_domain, DiatonicPitch(4, DiatonicToneCache.get_tone('A')), r, FlipType.CenterTone)

        print('f={0}'.format(f))

        TestFlipOnTonality.print_map('test_simple_pitch_function', f)

        t = f.tonal_function

        assert 'E' == t['D#'].diatonic_symbol
        assert 'F#' == t['C#'].diatonic_symbol
        assert 'G#' == t['B'].diatonic_symbol
        assert 'A' == t['A'].diatonic_symbol
        assert 'B' == t['G#'].diatonic_symbol
        assert 'C#' == t['F#'].diatonic_symbol
        assert 'D#' == t['E'].diatonic_symbol

        assert 'D#:5' == str(f['E:4'])
        assert 'C#:5' == str(f['F#:4'])
        assert 'A:4' == str(f['A:4'])
        assert 'G#:4' == str(f['B:4'])
        assert 'F#:4' == str(f['C#:5'])
        assert 'E:4' == str(f['D#:5'])

    def test_centered_even_function(self):
        t_domain = Tonality.create(ModalityType.HWOctatonic, DiatonicTone('C'))
        r = PitchRange.create('E:3', 'E:7')

        f = DiatonicPitchReflectionFunction(t_domain, DiatonicPitch(4, DiatonicToneCache.get_tone('A')), r, FlipType.CenterTone)

        TestFlipOnTonality.print_map('test_centered_even_function', f)

        t = f.tonal_function

        assert 'C' == t['Gb'].diatonic_symbol
        assert 'Db' == t['Fb'].diatonic_symbol
        assert 'Eb' == t['Eb'].diatonic_symbol
        assert 'Fb' == t['Db'].diatonic_symbol
        assert 'Gb' == t['C'].diatonic_symbol
        assert 'G' == t['Bb'].diatonic_symbol
        assert 'A' == t['A'].diatonic_symbol
        assert 'Bb' == t['G'].diatonic_symbol

        assert 'C:4' == str(f['Gb:5'])
        assert 'Db:4' == str(f['Fb:5'])

        assert 'Eb:4' == str(f['Eb:5'])  # The other stable tone outside of the centered!

        assert 'Fb:4' == str(f['Db:5'])
        assert 'Gb:4' == str(f['C:5'])
        assert 'G:4' == str(f['Bb:4'])
        assert 'A:4' == str(f['A:4'])
        assert 'Bb:4' == str(f['G:4'])
        assert 'C:5' == str(f['Gb:4'])
        assert 'Db:5' == str(f['Fb:4'])

    def test_non_centered_odd_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('E'))
        r = PitchRange.create('E:3', 'E:7')

        f = DiatonicPitchReflectionFunction(t_domain, DiatonicPitch(4, DiatonicToneCache.get_tone('F#')), r,
                                            FlipType.LowerNeighborOfPair)

        TestFlipOnTonality.print_map('test_non_centered_odd_function', f)

        t = f.tonal_function

        assert 'E' == t['A'].diatonic_symbol
        assert 'F#' == t['G#'].diatonic_symbol
        assert 'G#' == t['F#'].diatonic_symbol
        assert 'A' == t['E'].diatonic_symbol
        assert 'B' == t['D#'].diatonic_symbol
        assert 'C#' == t['C#'].diatonic_symbol
        assert 'D#' == t['B'].diatonic_symbol

        assert 'C#:4' == str(f['C#:5'])
        assert 'D#:4' == str(f['B:4'])
        assert 'E:4' == str(f['A:4'])
        assert 'F#:4' == str(f['G#:4'])
        assert 'G#:4' == str(f['F#:4'])
        assert 'A:4' == str(f['E:4'])
        assert 'B:4' == str(f['D#:4'])
        assert 'C#:5' == str(f['C#:4'])
        assert 'D#:5' == str(f['B:3'])

    def test_non_centered_even_function(self):
        t_domain = Tonality.create(ModalityType.WholeTone, DiatonicTone('C'))
        r = PitchRange.create('E:3', 'E:7')

        f = DiatonicPitchReflectionFunction(t_domain, DiatonicPitch(4, DiatonicToneCache.get_tone('G#')), r,
                                            FlipType.UpperNeighborOfPair)

        TestFlipOnTonality.print_map('test_non_centered_even_function', f)

        t = f.tonal_function

        assert 'C' == t['D'].diatonic_symbol
        assert 'D' == t['C'].diatonic_symbol
        assert 'E' == t['A#'].diatonic_symbol
        assert 'F#' == t['G#'].diatonic_symbol
        assert 'G#' == t['F#'].diatonic_symbol
        assert 'A#' == t['E'].diatonic_symbol

        assert 'C:4' == str(f['D:5'])
        assert 'D:4' == str(f['C:5'])
        assert 'E:4' == str(f['A#:4'])
        assert 'F#:4' == str(f['G#:4'])
        assert 'G#:4' == str(f['F#:4'])
        assert 'A#:4' == str(f['E:4'])
        assert 'C:5' == str(f['D:4'])

    def test_find_pitch(self):

        t_domain = Tonality.create(ModalityType.WholeTone, DiatonicTone('C'))
        r = PitchRange.create('E:1', 'E:7')

        f = DiatonicPitchReflectionFunction(t_domain, DiatonicPitch(4, DiatonicToneCache.get_tone('G#')), r,
                                            FlipType.UpperNeighborOfPair)

        TestFlipOnTonality.print_map('test_find_pitch', f)

        for t in t_domain.annotation:
            p = DiatonicPitch(1, t)
            closest_pitch, closest_distance = f._find_closest_pitch(p)
            print('pitch {0}  closest = ({1}, {2})'.format(p, closest_pitch, closest_distance))

        p = DiatonicPitch.parse("A:3")
        closest_pitch, closest_distance = f._find_closest_pitch(p)
        print('pitch {0}  closest = ({1}, {2})'.format(p, closest_pitch, closest_distance))

        p = DiatonicPitch.parse("Ab:3")
        closest_pitch, closest_distance = f._find_closest_pitch(p)
        print('pitch {0}  closest = ({1}, {2})'.format(p, closest_pitch, closest_distance))

        p = DiatonicPitch.parse("B:3")
        closest_pitch, closest_distance = f._find_closest_pitch(p)
        print('pitch {0}  closest = ({1}, {2})'.format(p, closest_pitch, closest_distance))

        p = DiatonicPitch.parse("Cb:3")
        closest_distance = f._find_closest_pitch(p)
        print('pitch {0}  closest = ({1}, {2})'.format(p, closest_pitch, closest_distance))

        p = DiatonicPitch.parse("C#:3")
        closest_pitch, closest_distance = f._find_closest_pitch(p)
        print('pitch {0}  closest = ({1}, {2})'.format(p, closest_pitch, closest_distance))

    def test_check_chromatics_on_c(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))
        r = PitchRange.create('E:1', 'E:7')

        f = DiatonicPitchReflectionFunction(t_domain, DiatonicPitch(4, DiatonicToneCache.get_tone('G')), r,
                                            FlipType.CenterTone)
        TestFlipOnTonality.print_map('test_check_chromatics_on_c', f)

        pitch = f['C#:4']
        print('Map {0} --> {1}'.format('C#:4', pitch))
        # assert 'Db:5' == f['C#:4']
        pitch = f['D#:4']
        print('Map {0} --> {1}'.format('D#:4', pitch))
        pitch = f['E#:4']
        print('Map {0} --> {1}'.format('E#:4', pitch))
        pitch = f['F#:4']
        print('Map {0} --> {1}'.format('F#:4', pitch))
        pitch = f['G#:4']
        print('Map {0} --> {1}'.format('G#:4', pitch))
        pitch = f['A#:4']
        print('Map {0} --> {1}'.format('A#:4', pitch))
        pitch = f['B#:4']
        print('Map {0} --> {1}'.format('B#:4', pitch))

        pitch = f['Cb:4']
        print('Map {0} --> {1}'.format('Cb:4', pitch))
        pitch = f['Db:4']
        print('Map {0} --> {1}'.format('Db:4', pitch))
        pitch = f['Eb:4']
        print('Map {0} --> {1}'.format('Eb:4', pitch))
        pitch = f['Fb:4']
        print('Map {0} --> {1}'.format('Fb:4', pitch))
        pitch = f['Gb:4']
        print('Map {0} --> {1}'.format('Gb:4', pitch))
        pitch = f['Ab:4']
        print('Map {0} --> {1}'.format('Ab:4', pitch))
        pitch = f['Bb:4']
        print('Map {0} --> {1}'.format('Bb:4', pitch))

    def test_check_chromatics_on_pentatonic(self):
        t_domain = Tonality.create(ModalityType.MajorPentatonic, DiatonicTone('E'))
        # E F# G# B C# E
        r = PitchRange.create('E:1', 'E:7')

        f = DiatonicPitchReflectionFunction(t_domain, DiatonicPitch(4, DiatonicToneCache.get_tone('G#')), r,
                                            FlipType.CenterTone)
        TestFlipOnTonality.print_map('test_check_chromatics_on_pentatonic', f)

        t = f.tonal_function
        assert 'G#' == t['G#'].diatonic_symbol
        assert 'F#' == t['B'].diatonic_symbol
        assert 'E' == t['C#'].diatonic_symbol
        assert 'B' == t['F#'].diatonic_symbol
        assert 'C#' == t['E'].diatonic_symbol

        assert 'E:4' == str(f['C#:5'])
        assert 'F#:4' == str(f['B:4'])
        assert 'G#:4' == str(f['G#:4'])
        assert 'B:4' == str(f['F#:4'])
        assert 'C#:5' == str(f['E:4'])

        assert 'E#:5' == str(f['C:4'])
        assert 'D#:5' == str(f['D:4'])
        assert 'B#:4' == str(f['F:4'])
        assert 'G##:4' == str(f['G:4'])  # Note this and next are not symmetrical!
        assert 'G:4' == str(f['A#:4'])
        assert 'F##:4' == str(f['A:4'])

        assert 'E##:5' == str(f['Cb:4'])
        assert 'D##:5' == str(f['Db:4'])
        assert 'C##:5' == str(f['Eb:4'])
        assert 'B##:4' == str(f['Fb:4'])
        assert 'G###:4' == str(f['Gb:4'])
        assert 'F###:4' == str(f['Ab:4'])   # Very interesting case!!! closest is G#, but need F# to get to G#
        assert 'F##:4' == str(f['Bb:4'])

        assert 'F:4' == str(f['B#:4'])
        assert 'D:5' == str(f['D#:4'])
        assert 'C:5' == str(f['E#:4'])
        assert 'G:4' == str(f['A#:4'])

    @staticmethod
    def print_map(tag, fctn):
        print(tag)
        keys = sorted([i for i in fctn.map.keys()])
        for key in keys:
            print('{0} --> {1}'.format(key, fctn[key]))
