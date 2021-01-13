import logging
import sys
import unittest

from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.tonality import Tonality
from transformation.functions.pitchfunctions.tonality_pitch_function import TonalityPitchFunction
from transformation.functions.tonalfunctions.tonality_permutation_function import TonalityPermutationFunction


class TestTonalityPitchFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_pitch_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('E'))
        cycles = [['E', 'G#', 'A', 'C#'], ('F#', 'D#')]
        permutation_function = TonalityPermutationFunction.create(t_domain, cycles)

        r = PitchRange.create('E:3', 'E:7')
        f = TonalityPitchFunction(permutation_function, ('E:4', 'E:5'), r)

        TestTonalityPitchFunction.print_map('test_simple_pitch_fnction', f)

        assert 'G#:5' == str(f['E:4'])
        assert 'D#:6' == str(f['F#:4'])
        assert 'A:5' == str(f['G#:4'])
        assert 'C#:6' == str(f['A:4'])
        assert 'B:5' == str(f['B:4'])
        assert 'E:5' == str(f['C#:5'])
        assert 'F#:5' == str(f['D#:5'])

    def test_simple_reverse_pitch_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('E'))
        cycles = [['E', 'G#', 'A', 'C#'], ('F#', 'D#')]
        permutation_function = TonalityPermutationFunction.create(t_domain, cycles)

        r = PitchRange.create('E:3', 'E:7')
        f = TonalityPitchFunction(permutation_function, ('E:4', 'E:5'), r, True)

        TestTonalityPitchFunction.print_map('test_simple_reverse_pitch_fnction', f)

        assert 'G#:5' == str(f['E:4'])
        assert 'D#:6' == str(f['F#:4'])
        assert 'A:5' == str(f['G#:4'])
        assert 'C#:6' == str(f['A:4'])
        assert 'B:5' == str(f['B:4'])
        assert 'E:5' == str(f['C#:5'])
        assert 'F#:5' == str(f['D#:5'])

        assert 'G#:4' == str(f['E:5'])
        assert 'D#:5' == str(f['F#:5'])
        assert 'A:4' == str(f['G#:5'])
        assert 'C#:5' == str(f['A:5'])
        assert 'B:4' == str(f['B:5'])
        assert 'E:4' == str(f['C#:6'])
        assert 'F#:4' == str(f['D#:6'])

    def test_forward_with_extension(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('E'))
        cycles = [['E', 'G#', 'A', 'C#'], ('F#', 'D#')]

        extension = dict()
        extension['D'] = 'F'
        extension['F'] = 'G'
        permutation_function = TonalityPermutationFunction.create(t_domain, cycles, extension)

        r = PitchRange.create('E:3', 'E:7')
        f = TonalityPitchFunction(permutation_function, ('E:4', 'E:5'), r, False)

        TestTonalityPitchFunction.print_map('test_forward_with_extension', f)

        assert 'G#:5' == str(f['E:4'])
        assert 'G:5' == str(f['F:4'])
        assert 'D#:6' == str(f['F#:4'])
        assert 'A:5' == str(f['G#:4'])
        assert 'C#:6' == str(f['A:4'])
        assert 'B:5' == str(f['B:4'])
        assert 'E:5' == str(f['C#:5'])
        assert 'E:5' == str(f['B##:4'])
        assert 'F:5' == str(f['D:5'])
        assert 'F:5' == str(f['C##:5'])
        assert 'F#:5' == str(f['D#:5'])

    def test_reversal_tonal_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('G'))
        cycles = [['C'], ['B', 'D'], ['E', 'A'], ['G', 'F#']]

        permutation_function = TonalityPermutationFunction.create(t_domain, cycles)

        r = PitchRange.create('E:3', 'E:7')
        f = TonalityPitchFunction(permutation_function, ('E:4', 'E:4'), r, True)

        TestTonalityPitchFunction.print_map('test_reversal_tonal_function', f)

        assert 'C:5' == str(f['C:5'])

    @staticmethod
    def print_map(tag, fctn):
        print(tag)
        keys = sorted([i for i in fctn.map.keys()])
        for key in keys:
            print('{0} --> {1}'.format(key, fctn[key]))
