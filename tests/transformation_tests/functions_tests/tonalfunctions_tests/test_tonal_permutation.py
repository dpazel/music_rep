import logging
import sys
import unittest

from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from transformation.functions.tonalfunctions.tonal_permutation import TonalPermutation


class TestTonalPermutation(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_tonal_permutation(self):
        domain = {'C', 'D', 'Eb', 'F#'}
        cycles = [['C', 'D'], ['Eb', 'F#']]
        p = TonalPermutation(cycles, domain)

        assert DiatonicToneCache.get_tone('C') in p.tone_domain
        assert DiatonicToneCache.get_tone('D') in p.tone_domain
        assert DiatonicToneCache.get_tone('Eb') in p.tone_domain
        assert DiatonicToneCache.get_tone('F#') in p.tone_domain

        assert DiatonicToneCache.get_tone('D') == p['C']
        assert DiatonicToneCache.get_tone('C') == p['D']
        assert DiatonicToneCache.get_tone('Eb') == p['F#']
        assert DiatonicToneCache.get_tone('F#') == p['Eb']

    def test_empty_tonal_permutation(self):
        p = TonalPermutation(None)

        assert isinstance(p.tone_domain, set)
        assert len(p.tone_domain) == 0
        assert isinstance(p.cycles, list)
        assert len(p.cycles) == 0

    def test_only_cycles(self):
        cycles = [['C', 'D'], ['Eb', 'F#']]
        p = TonalPermutation(cycles)

        assert DiatonicToneCache.get_tone('C') in p.tone_domain
        assert DiatonicToneCache.get_tone('D') in p.tone_domain
        assert DiatonicToneCache.get_tone('Eb') in p.tone_domain
        assert DiatonicToneCache.get_tone('F#') in p.tone_domain

        assert DiatonicToneCache.get_tone('D') == p['C']
        assert DiatonicToneCache.get_tone('C') == p['D']
        assert DiatonicToneCache.get_tone('Eb') == p['F#']
        assert DiatonicToneCache.get_tone('F#') == p['Eb']
