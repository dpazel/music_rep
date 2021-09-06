import logging
import sys
import unittest

from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from transformation.functions.tonalfunctions.tonal_function import TonalFunction


class TestTonalFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_tonal_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))
        t_range = Tonality.create(ModalityType.Major, DiatonicTone('A'))

        # default map between 2 tonalities of same cardinality.
        f = TonalFunction(t_domain, t_range)

        assert DiatonicToneCache.get_tone('A') == f['C']
        assert DiatonicToneCache.get_tone('B') == f['D']
        assert DiatonicToneCache.get_tone('C#') == f['E']
        assert DiatonicToneCache.get_tone('D') == f['F']
        assert DiatonicToneCache.get_tone('E') == f['G']
        assert DiatonicToneCache.get_tone('F#') == f['A']
        assert DiatonicToneCache.get_tone('G#') == f['B']

        skeleton = f.extract_template()
        assert [0, 1, 2, 3, 4, 5, 6] == skeleton.tonal_order

        TestTonalFunction.print_function(f)

    def test_defined_map(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))
        t_range = Tonality.create(ModalityType.MelodicMinor, DiatonicTone('A'))

        pmap = {'C': 'A', 'D': 'B', 'E': 'C', 'F': 'D', 'G': 'E', 'A': 'F#', 'B': 'G#'}

        # default map between 2 tonalities of same cardinality.
        f = TonalFunction(t_domain, t_range, pmap)

        assert DiatonicToneCache.get_tone('A') == f['C']
        assert DiatonicToneCache.get_tone('B') == f['D']
        assert DiatonicToneCache.get_tone('C') == f['E']
        assert DiatonicToneCache.get_tone('D') == f['F']
        assert DiatonicToneCache.get_tone('E') == f['G']
        assert DiatonicToneCache.get_tone('F#') == f['A']
        assert DiatonicToneCache.get_tone('G#') == f['B']

    def test_setting_values(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))
        t_range = Tonality.create(ModalityType.MajorPentatonic, DiatonicTone('A'))
        # A, B, C#, E, F#

        # default map between 2 tonalities of unequal cardinality - empty
        p = {'C': 'A', 'D': 'A', 'E': 'B', 'F': 'C#', 'G': 'C#', 'A': 'E', 'B': 'F#'}
        f = TonalFunction(t_domain, t_range, p)

        assert DiatonicToneCache.get_tone('A') == f['C']
        assert DiatonicToneCache.get_tone('A') == f['D']
        assert DiatonicToneCache.get_tone('B') == f['E']
        assert DiatonicToneCache.get_tone('C#') == f['F']
        assert DiatonicToneCache.get_tone('C#') == f['G']
        assert DiatonicToneCache.get_tone('E') == f['A']
        assert DiatonicToneCache.get_tone('F#') == f['B']

        assert [0, 0, 1, 2, 2, 3, 4] == f.extract_template().tonal_order

        f['C'] = 'B'
        f['D'] = 'A'
        f['E'] = 'C#'
        f['F'] = 'C#'
        f['G'] = 'F#'
        f['A'] = 'A'
        f['B'] = 'E'

        # del f['D']
        # assert f['D'] is None

        assert [1, 0, 2, 2, 4, 0, 3] == f.extract_template().tonal_order

        f['C#'] = 'B#'
        f['Db'] = 'Ab'
        f['A#'] = 'Eb'

        assert DiatonicToneCache.get_tone('B#') == f['C#']
        assert DiatonicToneCache.get_tone('Ab') == f['Db']
        assert DiatonicToneCache.get_tone('Eb') == f['A#']

        del f['Db']

    def test_extension_map(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))
        t_range = Tonality.create(ModalityType.Major, DiatonicTone('A'))

        extension_map = {'C#': 'A#', 'D#': 'C', 'Gb': 'G#'}

        # default map between 2 tonalities of same cardinality.
        f = TonalFunction(t_domain, t_range, None, extension_map)
        assert DiatonicToneCache.get_tone('A') == f['C']
        assert DiatonicToneCache.get_tone('B') == f['D']
        assert DiatonicToneCache.get_tone('C#') == f['E']
        assert DiatonicToneCache.get_tone('D') == f['F']
        assert DiatonicToneCache.get_tone('E') == f['G']
        assert DiatonicToneCache.get_tone('F#') == f['A']
        assert DiatonicToneCache.get_tone('G#') == f['B']

        assert f['Db'] is None
        assert DiatonicToneCache.get_tone('A#') == f['C#']
        assert DiatonicToneCache.get_tone('C') == f['D#']
        assert f['Eb'] is None
        assert DiatonicToneCache.get_tone('G#') == f['Gb']
        assert f['F#'] is None

    def test_simplified_adapted_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('F'))
        t_range = Tonality.create(ModalityType.MelodicMinor, DiatonicTone('G'))

        f = TonalFunction(t_domain, t_range)

        nt_domain = Tonality.create(ModalityType.Major, DiatonicTone('Ab'))
        nt_range = Tonality.create(ModalityType.MelodicMinor, DiatonicTone('e'))

        pf = f.create_adapted_function(nt_domain, nt_range)

        assert DiatonicToneCache.get_tone('E') == pf['Ab']
        assert DiatonicToneCache.get_tone('F#') == pf['Bb']
        assert DiatonicToneCache.get_tone('G') == pf['C']
        assert DiatonicToneCache.get_tone('A') == pf['Db']
        assert DiatonicToneCache.get_tone('B') == pf['Eb']
        assert DiatonicToneCache.get_tone('C#') == pf['F']
        assert DiatonicToneCache.get_tone('D#') == pf['G']



    def test_adapted_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('F'))
        t_range = Tonality.create(ModalityType.MelodicMinor, DiatonicTone('G'))

        pmap = {'F': 'G', 'G': 'F#', 'A': 'E', 'Bb': 'A', 'C': 'D', 'D': 'Bb', 'E': 'C'}
        f = TonalFunction(t_domain, t_range, pmap)

        nt_domain = Tonality.create(ModalityType.Major, DiatonicTone('Ab'))
        nt_range = Tonality.create(ModalityType.MelodicMinor, DiatonicTone('e'))

        pf = f.create_adapted_function(nt_domain, nt_range)

        assert 'E' == str(pf['Ab'].diatonic_symbol)
        assert 'D#' == str(pf['Bb'].diatonic_symbol)
        assert 'C#' == str(pf['C'].diatonic_symbol)
        assert 'F#' == str(pf['Db'].diatonic_symbol)
        assert 'B' == str(pf['Eb'].diatonic_symbol)
        assert 'G' == str(pf['F'].diatonic_symbol)
        assert 'A' == str(pf['G'].diatonic_symbol)

        # Test chromatics
        f['G#'] = 'F##'
        f['Gb'] = 'F'
        f['B'] = 'Db'  # aug 4th --> dim 5th

        pf = f.create_adapted_function(nt_domain, nt_range)

        assert 'D##' == str(pf['B'].diatonic_symbol)
        assert 'Bb' == str(pf['D'].diatonic_symbol)  # D is aug 4th in Ab; Bb is dim 5th in e minor

    def print_function(f):
        domain_tonality = f.domain_tonality
        tones = domain_tonality.annotation[:len(domain_tonality.annotation) - 1]

        for t in tones:
            print('{0} --> {1}'.format(t.diatonic_symbol, f[t].diatonic_symbol))
