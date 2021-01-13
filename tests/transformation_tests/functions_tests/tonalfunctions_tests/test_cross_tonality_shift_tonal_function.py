import logging
import sys
import unittest

from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.interval import Interval, IntervalType
from transformation.functions.tonalfunctions.cross_tonality_shift_tonal_function import \
    CrossTonalityShiftTonalFunction
from tonalmodel.diatonic_foundation import DiatonicFoundation


class TestCrossTonalityShiftTonalFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_intervallic_tonal_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('C'))

        f = CrossTonalityShiftTonalFunction(t_domain, 'F')

        assert 'F' == f['C'].diatonic_symbol
        assert 'G' == f['D'].diatonic_symbol
        assert 'A' == f['E'].diatonic_symbol
        assert 'Bb' == f['F'].diatonic_symbol
        assert 'C' == f['G'].diatonic_symbol
        assert 'D' == f['A'].diatonic_symbol
        assert 'E' == f['B'].diatonic_symbol

        assert 'Fb' == f['Cb'].diatonic_symbol
        assert 'F#' == f['C#'].diatonic_symbol
        assert 'B' == f['F#'].diatonic_symbol
        assert 'Eb' == f['Bb'].diatonic_symbol
        assert 'E#' == f['B#'].diatonic_symbol

        assert 'Ebb' == f['Bbb'].diatonic_symbol
        assert 'E##' == f['B##'].diatonic_symbol

        assert 'Bbbb' == f['Fbb'].diatonic_symbol

    def test_modal_intervallic_tonal_function(self):
        t_domain = Tonality.create(ModalityType.Major, DiatonicTone('Ab'))

        f = CrossTonalityShiftTonalFunction(t_domain, 'F#', 2)

        assert 'D' == f.range_tonality.basis_tone.diatonic_symbol
        assert 'F#' == f.range_tonality.root_tone.diatonic_symbol

        assert 'F#' == f['Ab'].diatonic_symbol
        assert 'G' == f['Bb'].diatonic_symbol
        assert 'A' == f['C'].diatonic_symbol
        assert 'B' == f['Db'].diatonic_symbol
        assert 'C#' == f['Eb'].diatonic_symbol
        assert 'D' == f['f'].diatonic_symbol
        assert 'E' == f['g'].diatonic_symbol

        assert 'G#' == f['B'].diatonic_symbol
        assert 'G##' == f['B#'].diatonic_symbol
        assert 'G###' == f['B##'].diatonic_symbol

    def test_pentatonic_tonal_function(self):
        t_domain = Tonality.create(ModalityType.MajorPentatonic, DiatonicTone('C'))

        interval = Interval(3, IntervalType.Major)

        f = CrossTonalityShiftTonalFunction.create_shift(t_domain, interval)
        # C, D, E, G. A ==> E, F#, G#, B, C#

        assert 'E' == f['C'].diatonic_symbol
        assert 'F#' == f['D'].diatonic_symbol
        assert 'G#' == f['E'].diatonic_symbol
        assert 'B' == f['G'].diatonic_symbol
        assert 'C#' == f['A'].diatonic_symbol

        assert 'A' == f['F'].diatonic_symbol
        assert 'D#' == f['B'].diatonic_symbol

        assert 'A#' == f['F#'].diatonic_symbol
        assert 'D##' == f['B#'].diatonic_symbol
        assert 'Ab' == f['Fb'].diatonic_symbol
        assert 'D' == f['Bb'].diatonic_symbol

        t_range = Tonality.create(ModalityType.MajorPentatonic, interval.get_end_tone(DiatonicTone('C')))
        f = CrossTonalityShiftTonalFunction(t_domain, t_range.annotation[2], 2)
        # C, D, E, G. A ==> G#, B, C#, E, F#

        assert 'G#' == f['C'].diatonic_symbol
        assert 'B' == f['D'].diatonic_symbol
        assert 'C#' == f['E'].diatonic_symbol
        assert 'E' == f['G'].diatonic_symbol
        assert 'F#' == f['A'].diatonic_symbol

        TestCrossTonalityShiftTonalFunction.print_function(f)

    def print_function(f):
        domain_tonality = f.domain_tonality
        tones = domain_tonality.annotation[:len(domain_tonality.annotation) - 1]

        for t in tones:
            print('{0} --> {1}'.format(t.diatonic_symbol, f[t].diatonic_symbol))

        print('------------------------')
        #print for domain tone letters not int the domain tonality

        for l in 'ABCDEFG':
            found = False
            for t in tones:
                if t.diatonic_letter == l:
                    found = True
                    break
            if not found:
                ltr_tone = DiatonicFoundation.get_tone(l)
                print('{0} --> {1}'.format(ltr_tone.diatonic_symbol, f[ltr_tone].diatonic_symbol))