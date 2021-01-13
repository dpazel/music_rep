import logging
import sys
import unittest

from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from transformation.functions.tonalfunctions.chromatic_permutation import ChromaticPermutation


class TestChromaticPermutation(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_id_chromatic_permutation(self):
        c = ChromaticPermutation()
        print(c)

        assert DiatonicToneCache.get_tone('C') == c['C']
        assert DiatonicToneCache.get_tone('C#') == c['C#']
        assert DiatonicToneCache.get_tone('D') == c['D']
        assert DiatonicToneCache.get_tone('D#') == c['D#']
        assert DiatonicToneCache.get_tone('E') == c['E']
        assert DiatonicToneCache.get_tone('F') == c['F']
        assert DiatonicToneCache.get_tone('F#') == c['F#']
        assert DiatonicToneCache.get_tone('G') == c['G']
        assert DiatonicToneCache.get_tone('G#') == c['G#']
        assert DiatonicToneCache.get_tone('A') == c['A']
        assert DiatonicToneCache.get_tone('A#') == c['A#']
        assert DiatonicToneCache.get_tone('B') == c['B']

    def test_normalized_permuationa(self):
        cycles = [['c', 'e', 'g', 'f#'], ['g', 'b']]
        c = ChromaticPermutation(cycles)
        print(c)

        assert DiatonicToneCache.get_tone('E') == c['C']
        assert DiatonicToneCache.get_tone('C#') == c['C#']
        assert DiatonicToneCache.get_tone('D') == c['D']
        assert DiatonicToneCache.get_tone('D#') == c['D#']
        assert DiatonicToneCache.get_tone('G') == c['E']
        assert DiatonicToneCache.get_tone('F') == c['F']
        assert DiatonicToneCache.get_tone('C') == c['F#']
        assert DiatonicToneCache.get_tone('B') == c['G']
        assert DiatonicToneCache.get_tone('G#') == c['G#']
        assert DiatonicToneCache.get_tone('A') == c['A']
        assert DiatonicToneCache.get_tone('A#') == c['A#']
        assert DiatonicToneCache.get_tone('F#') == c['B']

    def test_non_normalized_permutation(self):
        cycles = [['c', 'e', 'g', 'gb'], ['f##', 'bb']]
        c = ChromaticPermutation(cycles)
        print(c)

        assert DiatonicToneCache.get_tone('E') == c['C']
        assert DiatonicToneCache.get_tone('C#') == c['C#']
        assert DiatonicToneCache.get_tone('D') == c['D']
        assert DiatonicToneCache.get_tone('D#') == c['D#']
        assert DiatonicToneCache.get_tone('G') == c['E']
        assert DiatonicToneCache.get_tone('F') == c['F']
        assert DiatonicToneCache.get_tone('C') == c['F#']
        assert DiatonicToneCache.get_tone('Bb') == c['G']
        assert DiatonicToneCache.get_tone('G#') == c['G#']
        assert DiatonicToneCache.get_tone('A') == c['A']
        assert DiatonicToneCache.get_tone('Gb') == c['A#']
        assert DiatonicToneCache.get_tone('B') == c['B']
