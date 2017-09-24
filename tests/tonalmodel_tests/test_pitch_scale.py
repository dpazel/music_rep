import unittest

from tonalmodel.tonality import Tonality
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.pitch_scale import PitchScale
from tonalmodel.modality_factory import ModalityFactory
from tonalmodel.diatonic_foundation import DiatonicFoundation


def get_symbol(dt):
    return str(dt)


def scale_check(pitch_scale, tonality):
    tones = tonality.annotation
    if len(pitch_scale.pitch_scale) == 0:
        print()
    scale_pitch = pitch_scale.pitch_scale[0]
    tone_index = tones.index(scale_pitch.diatonic_tone)

    for scale_pitch in pitch_scale.pitch_scale[1:]:
        tone_index = (tone_index + 1) % (len(tones) - 1)
        assert scale_pitch.diatonic_tone == tones[tone_index], \
            '{0} != {1}'.format(scale_pitch.diatonic_tone, tones[tone_index])


class TestTonalScale(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_scale(self):
        ranges = PitchRange.create("Bb:4", "C#:6")
        
        for modality_type in range(21):
            for validTone in ModalityFactory.create_modality(modality_type).get_valid_root_tones():
                tonality = Tonality(modality_type, DiatonicFoundation.get_tone(validTone))               
                                
                if modality_type == 3 and str(validTone) == 'Db':
                    print()
        
                pitch_scale = PitchScale(tonality, ranges)
                print('Scale {0} {1} on {2}: {3}'.format(validTone, str(ModalityType(modality_type)), ranges,
                                                         ','.join(map(get_symbol, pitch_scale.pitch_scale))))

                scale_check(pitch_scale, tonality)
                
    def test_low_range(self):
        ranges = PitchRange.create("A:0", "C:5")
        for modality_type in range(21):
            for validTone in ModalityFactory.create_modality(modality_type).get_valid_root_tones():
                tonality = Tonality(modality_type, DiatonicFoundation.get_tone(validTone))
        
                pitch_scale = PitchScale(tonality, ranges)
                print('Scale {0} {1} on {2}: {3}'.format(validTone, str(ModalityType(modality_type)), ranges,
                                                         ','.join(map(get_symbol, pitch_scale.pitch_scale))))

                scale_check(pitch_scale, tonality)
                
    def test_hi_range(self):
        ranges = PitchRange.create("c:4", "c:8")
        for modality_type in range(21):
            for validTone in ModalityFactory.create_modality(modality_type).get_valid_root_tones():
                tonality = Tonality(modality_type, DiatonicFoundation.get_tone(validTone))
                
                if modality_type == 0 and str(validTone) == 'D':
                    print()
        
                pitch_scale = PitchScale(tonality, ranges)
                print('Scale {0} {1} on {2}: {3}'.format(validTone, str(ModalityType(modality_type)), ranges,
                                                         ','.join(map(get_symbol, pitch_scale.pitch_scale))))

                scale_check(pitch_scale, tonality)

if __name__ == "__main__":
    unittest.main()
