import logging
import sys
import unittest

from transformation.functions.tonalfunctions.tonality_permutation_function import TonalityPermutationFunction

from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from transformation.functions.tonalfunctions.tonality_permutation import TonalityPermutation


class TestTonalityPermutationFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_tonality_permutation_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('A'))
        cycles = [['C#', 'D'], ['E', 'G#']]
        p = TonalityPermutationFunction.create(t_domain, cycles)

        assert DiatonicToneCache.get_tone('C#') in p.domain
        assert DiatonicToneCache.get_tone('D') in p.domain
        assert DiatonicToneCache.get_tone('E') in p.domain
        assert DiatonicToneCache.get_tone('G#') in p.domain

        assert DiatonicToneCache.get_tone('D') == p['C#']
        assert DiatonicToneCache.get_tone('C#') == p['D']
        assert DiatonicToneCache.get_tone('E') == p['G#']
        assert DiatonicToneCache.get_tone('G#') == p['E']

        f = TonalityPermutationFunction(TonalityPermutation(t_domain, cycles))

        assert DiatonicToneCache.get_tone('C#') in f.domain
        assert DiatonicToneCache.get_tone('D') in f.domain
        assert DiatonicToneCache.get_tone('E') in f.domain
        assert DiatonicToneCache.get_tone('G#') in f.domain

        assert DiatonicToneCache.get_tone('D') == f['C#']
        assert DiatonicToneCache.get_tone('C#') == f['D']
        assert DiatonicToneCache.get_tone('E') == f['G#']
        assert DiatonicToneCache.get_tone('G#') == f['E']
