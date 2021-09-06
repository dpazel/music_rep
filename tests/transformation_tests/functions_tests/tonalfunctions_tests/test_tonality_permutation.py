import logging
import sys
import unittest

from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from transformation.functions.tonalfunctions.tonality_permutation import TonalityPermutation


class TestTonalityPermutation(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_tonal_permutation(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('E'))
        cycles = [['E', 'G#', 'A', 'B'], ('F#', 'G#')]
        p = TonalityPermutation(t_domain, cycles)

        assert DiatonicToneCache.get_tone('G#') == p['E']
        assert DiatonicToneCache.get_tone('A') == p['F#']
        assert DiatonicToneCache.get_tone('F#') == p['G#']
        assert DiatonicToneCache.get_tone('B') == p['A']
        assert DiatonicToneCache.get_tone('E') == p['B']
        assert DiatonicToneCache.get_tone('C#') == p['C#']
        assert DiatonicToneCache.get_tone('D#') == p['D#']

    def test_simple_id(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('E'))

        p = TonalityPermutation(t_domain)
        print(p)

        assert DiatonicToneCache.get_tone('E') == p['E']
        assert DiatonicToneCache.get_tone('F#') == p['F#']
        assert DiatonicToneCache.get_tone('G#') == p['G#']
        assert DiatonicToneCache.get_tone('A') == p['A']
        assert DiatonicToneCache.get_tone('B') == p['B']
        assert DiatonicToneCache.get_tone('C#') == p['C#']
        assert DiatonicToneCache.get_tone('D#') == p['D#']

