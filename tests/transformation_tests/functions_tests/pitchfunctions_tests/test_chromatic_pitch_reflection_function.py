import logging
import sys
import unittest

from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.tonality import Tonality
from transformation.functions.pitchfunctions.chromatic_pitch_reflection_function import ChromaticPitchReflectionFunction
from transformation.functions.pitchfunctions.diatonic_pitch_reflection_function import FlipType
from tonalmodel.diatonic_foundation import DiatonicFoundation


class TestChromaticPitchReflectionFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_major_modality(self):
        print('Testing Major Modality: D-Major, cue=G:4')
        domain_tonality = Tonality.create(ModalityType.Major, DiatonicFoundation.get_tone('D'))
        cue_pitch = DiatonicPitch.parse('G:4')

        domain_pitch_range = PitchRange.create('D:3', 'C#:6')
        f = ChromaticPitchReflectionFunction(domain_tonality, cue_pitch, domain_pitch_range, FlipType.CenterTone)

        TestChromaticPitchReflectionFunction.print_function(f)

        # Ensure all domain keys are in the domain_pitch_range
        for pitch in f.domain:
            assert domain_pitch_range.is_pitch_inbounds(pitch), \
                'Pitch {0} is not in range {1}.'.format(pitch, domain_pitch_range)

        assert DiatonicPitch.parse('D:3') in f.domain
        assert DiatonicPitch.parse('C#:6') in f.domain

        # Test for octave coverage
        assert 6 == f['D:3'].octave
        assert 5 == f['C#:4'].octave
        assert 5 == f['D:4'].octave
        assert 4 == f['C#:5'].octave
        assert 4 == f['D:5'].octave
        assert 3 == f['C#:6'].octave

    def test_melodic_minor_modality(self):
        print('Testing Melodic Minor Modality: C-MelodicMinor, cue=Eb:3')
        domain_tonality = Tonality.create(ModalityType.MelodicMinor, DiatonicFoundation.get_tone('C'))
        cue_pitch = DiatonicPitch.parse('Eb:3')

        domain_pitch_range = PitchRange.create('D:4', 'F:5')
        f = ChromaticPitchReflectionFunction(domain_tonality, cue_pitch, domain_pitch_range, FlipType.CenterTone)

        TestChromaticPitchReflectionFunction.print_function(f)

        assert 2 == f['D:4'].octave
        assert 2 == f['G:4'].octave
        assert 1 == f['A:4'].octave
        assert 1 == f['C:5'].octave
        assert 1 == f['f:5'].octave

    def test_natural_minor_modality(self):
        print('Testing Natural Minor Modality: C-Major, cue=Eb:3')
        domain_tonality = Tonality.create(ModalityType.NaturalMinor, DiatonicFoundation.get_tone('C'))
        cue_pitch = DiatonicPitch.parse('Eb:3')

        domain_pitch_range = PitchRange.create('D:2', 'F:4')
        f = ChromaticPitchReflectionFunction(domain_tonality, cue_pitch, domain_pitch_range, FlipType.CenterTone)

        TestChromaticPitchReflectionFunction.print_function(f)

        # Test for octave coverage
        assert 4 == f['D:2'].octave
        assert 3 == f['Bb:2'].octave
        assert 3 == f['C:3'].octave
        assert 2 == f['Bb:3'].octave
        assert 2 == f['F:4'].octave

    @staticmethod
    def print_function(f, only_scale=True):
        print('[{0}] ({1})  {2}'.format(f.domain_tonality, f.cue_pitch, f.range_tonality))
        domain = sorted([p for p in f.domain], key=lambda p: p.chromatic_distance)
        domain_tones = f.domain_tonality.annotation[:-1]
        for p in domain:
            r = f[p]
            if p.diatonic_tone in domain_tones:
                print('==> {0} --> {1}'.format(p, r))
            elif not only_scale:
                print('{0} --> {1}'.format(p, r))

        print()
