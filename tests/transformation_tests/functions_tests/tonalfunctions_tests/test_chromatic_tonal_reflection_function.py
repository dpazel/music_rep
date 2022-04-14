import logging
import sys
import unittest

from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from transformation.functions.pitchfunctions.diatonic_pitch_reflection_function import FlipType
from transformation.functions.tonalfunctions.chromatic_tonal_reflection_function import ChromaticTonalReflectionFunction


class TestChromaticTonalReflectionFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_C_major_modal_scales_center_cue(self):

        print('test_C_major_modal_scales_center_cue: CenterTone, cue == root tone, modal on C-Major')

        answers = [
            ['C', 'Bb', 'Ab', 'G', 'F', 'Eb', 'Db'],
            ['D', 'C', 'B', 'A', 'G', 'F', 'E'],
            ['E', 'D#', 'C#', 'B', 'A', 'G#', 'F#'],
            ['F', 'Eb', 'Db', 'Cb', 'Bb', 'Ab', 'Gb'],
            ['G', 'F', 'Eb', 'D', 'C', 'Bb', 'A'],
            ['A', 'G', 'F#', 'E', 'D', 'C#', 'B'],
            ['B', 'A#', 'G#', 'F#', 'E#', 'D#', 'C#']
        ]

        index = 0
        for letter in list('CDEFGAB'):
            modal_tonality = Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone(letter), index)
            f = ChromaticTonalReflectionFunction(modal_tonality, DiatonicToneCache.get_tone(letter),
                                                 FlipType.CenterTone)

            TestChromaticTonalReflectionFunction.print_map(modal_tonality, f, letter)
            for tone, i in zip(modal_tonality.annotation[:-1], range(0, 6)):
                assert f[tone] == DiatonicToneCache.get_tone(answers[index][i]), \
                    'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                               DiatonicToneCache.get_tone(answers[index][i]).diatonic_symbol)

            index = index + 1

    def test_C_Major_variable_cue_center_function(self):

        print('test_C_Major_variable_cue_center_function: C-Major, variable cue')
        domain_tonality = Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('C'))
        answers = [
            ['C', 'Bb', 'Ab', 'G', 'F', 'Eb', 'Db'],
            ['E', 'D', 'C', 'B', 'A', 'G', 'F'],
            ['G#', 'F#', 'E', 'D#', 'C#', 'B', 'A'],
            ['Bb', 'Ab', 'Gb', 'F', 'Eb', 'Db', 'Cb'],
            ['D', 'C', 'Bb', 'A', 'G', 'F', 'Eb'],
            ['F#', 'E', 'D', 'C#', 'B', 'A', 'B'],
            ['A#', 'G#', 'F#', 'E#', 'D#', 'C#', 'B']
        ]

        index = 0
        for letter in list('CDEFGAB'):
            f = ChromaticTonalReflectionFunction(domain_tonality, DiatonicToneCache.get_tone(letter),
                                                 FlipType.CenterTone)

            TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, letter)
            for tone, i in zip(domain_tonality.annotation[:-1], range(0, 6)):
                assert f[tone] == DiatonicToneCache.get_tone(answers[index][i]), \
                    'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                               DiatonicToneCache.get_tone(answers[index][i]).diatonic_symbol)
            index = index + 1

    def test_C_Major_variable_cue_lower_neighbor_function(self):
        print('test_C_Major_variable_cue_lower_neighbor_function: C-major, variable cue')
        domain_tonality = Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('C'))
        answers = [
            ['D', 'C', 'Bb', 'A', 'G', 'F', 'Eb'],
            ['F#', 'E', 'D', 'C#', 'B', 'A', 'G'],
            ['A', 'G', 'F', 'E', 'D', 'C', 'Bb'],
            ['C', 'Bb', 'Ab', 'G', 'F', 'Eb', 'Db'],
            ['E', 'D', 'C', 'B', 'A', 'G', 'G'],
            ['G#', 'F#', 'E', 'D#', 'C#', 'B', 'A'],
            ['B', 'A', 'G', 'F#', 'E', 'D', 'C']
        ]

        index = 0
        for letter in list('CDEFGAB'):
            f = ChromaticTonalReflectionFunction(domain_tonality, DiatonicToneCache.get_tone(letter),
                                                 FlipType.LowerNeighborOfPair)

            TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, letter)
            for tone, i in zip(domain_tonality.annotation[:-1], range(0, 6)):
                assert f[tone] == DiatonicToneCache.get_tone(answers[index][i]), \
                    'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                               DiatonicToneCache.get_tone(answers[index][i]).diatonic_symbol)

            index += 1

    def test_C_Major_variable_cue_upper_neighbor_function(self):
        print('test_C_Major_variable_cue_upper_neighbor_function: C-Major, variable cue')

        domain_tonality = Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('C'))
        answers = [
            ['B', 'A', 'G', 'F#', 'E', 'D', 'C'],
            ['D', 'C', 'Bb', 'A', 'G', 'F', 'Eb'],
            ['F#', 'E', 'D', 'C#', 'B', 'A', 'G'],
            ['A', 'G', 'F', 'E', 'D', 'C', 'Bb'],
            ['C', 'Bb', 'Ab', 'G', 'F', 'Eb', 'Db'],
            ['E', 'D', 'C', 'B', 'A', 'G', 'G'],
            ['G#', 'F#', 'E', 'D#', 'C#', 'B', 'A']
        ]

        index = 0
        for letter in list('CDEFGAB'):
            f = ChromaticTonalReflectionFunction(domain_tonality, DiatonicToneCache.get_tone(letter),
                                                 FlipType.UpperNeighborOfPair)

            TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, letter)
            for tone, i in zip(domain_tonality.annotation[:-1], range(0, 6)):
                assert f[tone] == DiatonicToneCache.get_tone(answers[index][i]), \
                    'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                               DiatonicToneCache.get_tone(answers[index][i]).diatonic_symbol)
            index += 1

    def test_C_Melodic_variable_cue_center(self):
        print('test_C_Melodic_variable_cue_center: C-Melodic, variable cue')

        domain_tonality = Tonality.create(ModalityType.MelodicMinor, DiatonicToneCache.get_tone('C'))
        answers = [
            ['C', 'Bb', 'A', 'G', 'F', 'Eb', 'Db'],
            ['E', 'D', 'C#', 'B', 'A', 'G', 'F'],
            ['Gb', 'Fb', 'Eb', 'Db', 'Cb', 'Bbb', 'Abb'],
            ['Bb', 'Ab', 'G', 'F', 'Eb', 'Db', 'Cb'],
            ['D', 'C', 'B', 'A', 'G', 'F', 'Eb'],
            ['F#', 'E', 'D#', 'C#', 'B', 'A', 'G'],
            ['A#', 'G#', 'F##', 'E#', 'D#', 'C#', 'B']
        ]

        index = 0
        for cue_tone in domain_tonality.annotation[:-1]:
            f = ChromaticTonalReflectionFunction(domain_tonality, cue_tone,
                                                 FlipType.CenterTone)

            TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, cue_tone.diatonic_symbol)
            for tone, i in zip(domain_tonality.annotation[:-1], range(0, 6)):
                assert f[tone] == DiatonicToneCache.get_tone(answers[index][i]), \
                     'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                                DiatonicToneCache.get_tone(answers[index][i]).diatonic_symbol)

            index += 1

    def test_C_Natural_variable_cue_center(self):
        print('test_C_Natural_variable_cue_center: C-Natural, variable cue')

        domain_tonality = Tonality.create(ModalityType.NaturalMinor, DiatonicToneCache.get_tone('C'))
        answers = [
            ['C', 'Bb', 'A', 'G', 'F', 'E', 'D'],
            ['E', 'D', 'C#', 'B', 'A', 'G#', 'F#'],
            ['Gb', 'Fb', 'Eb', 'Db', 'Cb', 'Bb', 'Ab'],
            ['Bb', 'Ab', 'G', 'F', 'Eb', 'D', 'C'],
            ['D', 'C', 'B', 'A', 'G', 'F#', 'E'],
            ['Fb', 'Ebb', 'Db', 'Cb', 'Bbb', 'Ab', 'Gb'],
            ['Ab', 'Gb', 'F', 'Eb', 'Db', 'C', 'Bb']
        ]

        index = 0
        for cue_tone in domain_tonality.annotation[:-1]:
            f = ChromaticTonalReflectionFunction(domain_tonality, cue_tone,
                                                 FlipType.CenterTone)

            TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, cue_tone.diatonic_symbol)
            for tone, i in zip(domain_tonality.annotation[:-1], range(0, 6)):
                assert f[tone] == DiatonicToneCache.get_tone(answers[index][i]), \
                     'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                                DiatonicToneCache.get_tone(answers[index][i]).diatonic_symbol)

            index += 1

    def test_C_harmonic_minor(self):
        print('test_C_harmonic_minor: C-Harmonic_Minor, variable cue')

        domain_tonality = Tonality.create(ModalityType.HarmonicMinor, DiatonicToneCache.get_tone('C'))
        tones = domain_tonality.annotation[:-1]
        cue_tone = tones[1]
        f = ChromaticTonalReflectionFunction(domain_tonality, cue_tone, FlipType.CenterTone)

        TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, cue_tone.diatonic_symbol)

        answers = ['E', 'D', 'C#', 'B', 'A', 'G#', 'F']
        for tone, i in zip(tones, range(0, 7)):
            assert f[tone] == DiatonicToneCache.get_tone(answers[i]), \
                'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                           DiatonicToneCache.get_tone(answers[i]).diatonic_symbol)

    def test_C_harmonic_major(self):
        print('test_C_harmonic_major: C-Harmonic_Majorr, variable cue')

        domain_tonality = Tonality.create(ModalityType.HarmonicMajor, DiatonicToneCache.get_tone('C'))
        tones = domain_tonality.annotation[:-1]
        cue_tone = tones[1]
        f = ChromaticTonalReflectionFunction(domain_tonality, cue_tone, FlipType.CenterTone)

        TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, cue_tone.diatonic_symbol)

        answers = ['E', 'D', 'C', 'B', 'A', 'G#', 'F']
        for tone, i in zip(tones, range(0, 7)):
            assert f[tone] == DiatonicToneCache.get_tone(answers[i]), \
               'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                          DiatonicToneCache.get_tone(answers[i]).diatonic_symbol)

    def test_C_pentatonic(self):
        print('test_C_pentatonic: C-Pentatonic, variable cue')

        domain_tonality = Tonality.create(ModalityType.MajorPentatonic, DiatonicToneCache.get_tone('C'))
        tones = domain_tonality.annotation[:-1]
        cue_tone = tones[1]
        f = ChromaticTonalReflectionFunction(domain_tonality, cue_tone, FlipType.CenterTone)

        TestChromaticTonalReflectionFunction.print_map(domain_tonality, f, cue_tone.diatonic_symbol)

        answers = ['E', 'D', 'C', 'A', 'G']
        for tone, i in zip(tones, range(0, 5)):
            assert f[tone] == DiatonicToneCache.get_tone(answers[i]), \
                'f[{0}]={1} != {2}'.format(tone.diatonic_symbol, f[tone].diatonic_symbol,
                                           DiatonicToneCache.get_tone(answers[i]).diatonic_symbol)

    @staticmethod
    def print_map(tonality, f, cue):
        map_list = list()
        for tone in tonality.annotation[:-1]:
            ft = f.tonal_map[tone]
            map_list.append('{0}-->{1}'.format(tone.diatonic_symbol, ft.diatonic_symbol))
        print('[{0}] ({1})  {2}'.format(cue, f.range_tonality, ', '.join([s for s in map_list])))
