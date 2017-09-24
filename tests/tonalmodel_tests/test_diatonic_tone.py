import unittest
from tonalmodel.diatonic_foundation import DiatonicFoundation


class TestDiatonicTone(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_diatonic_pitches(self):
        letters = list('CDEFGAB')
        augmentations = ('bb', 'b', '', '#', '##')
        diatonic_offsets = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        augmentation_offsets = {'': 0, 'b': -1, 'bb': -2, '#': 1, '##': 2}
        for ltr in letters:
            for aug in augmentations:
                diatonic_tone = DiatonicFoundation.get_tone(ltr + aug)

                assert diatonic_tone.diatonic_symbol == ltr + aug
                assert diatonic_tone.diatonic_letter == ltr
                assert diatonic_tone.augmentation_symbol == aug
                assert diatonic_tone.diatonic_index == letters.index(ltr)
                assert diatonic_tone.tonal_offset == diatonic_offsets[ltr] + augmentation_offsets[aug]
                assert diatonic_tone.augmentation_offset == augmentation_offsets[aug]

    def test_enharmonics(self):
        letters = list('CDEFGAB')
        augmentations = ('bb', 'b', '', '#', '##')
        for letter in letters:
            for aug in augmentations:
                l = letter + aug
                tone = DiatonicFoundation.get_tone(l)
                enharmonics = tone.enharmonics()
                print('{0}: {1}'.format(l, enharmonics))
                assert l in enharmonics

if __name__ == "__main__":
    unittest.main()
