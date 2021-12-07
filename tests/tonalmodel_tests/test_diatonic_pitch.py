import unittest
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone

class TestDiatonicPitch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_diatonic_pitches(self):
        letters = list('CDEFGAB')
        augmentations = ('bb', 'b', '', '#', '##')
        for octave in range(0, 8):
            for ltr in letters:
                for aug in augmentations:
                    diatonic_pitch = DiatonicPitch(octave, ltr + aug)

                    assert diatonic_pitch.diatonic_tone.diatonic_symbol == ltr + aug
                    assert diatonic_pitch.octave == octave

    def test_diatonic_pitches_using_parse(self):
        letters = list('CDEFGAB')
        augmentations = ('bb', 'b', '', '#', '##')
        for octave in range(0, 8):
            for ltr in letters:
                for aug in augmentations:
                    diatonic_pitch = DiatonicPitch.parse('{0}{1}:{2}'.format(ltr, aug, octave))

                    assert diatonic_pitch.diatonic_tone.diatonic_symbol == ltr + aug
                    assert diatonic_pitch.octave == octave

    def test_for_book(self):
        pitch = DiatonicPitch(5, 'Eb')
        print(pitch)
        pitch = DiatonicPitch.parse('Fb:3')
        print(pitch)