import unittest
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_tone import DiatonicTone


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
                tltrs = letter + aug
                tone = DiatonicFoundation.get_tone(tltrs)
                enharmonics = tone.enharmonics()
                print('{0}: {1}'.format(tltrs, enharmonics))
                assert tltrs in enharmonics

    def test_diatonic_distance(self):
        letters = list('CDEFGAB')
        augmentations = ('bb', 'b', '', '#', '##')
        for letter in letters:
            for aug in augmentations:
                tltrs = letter + aug
                tone1 = DiatonicFoundation.get_tone(tltrs)
                for letter2 in letters:
                    for aug2 in augmentations:
                        tltrs = letter2 + aug2
                        tone2 = DiatonicFoundation.get_tone(tltrs)
                        dd = DiatonicTone.calculate_diatonic_distance(tone1, tone2)
                        calc_dd = tone2.diatonic_index - tone1.diatonic_index \
                            if tone1.diatonic_index <= tone2.diatonic_index else \
                            tone2.diatonic_index - tone1.diatonic_index + 7
                        assert dd == calc_dd
                        print("{0} {1} {2}".format(tone1.diatonic_symbol, tone2.diatonic_symbol, dd))

    def test_chromatic_extension(self):
        inc = 2
        tone = DiatonicFoundation.get_tone('E')
        results = set()
        for i in range(tone.diatonic_index, tone.diatonic_index + inc):
            ltr = DiatonicTone.DIATONIC_LETTERS[i % len(DiatonicTone.DIATONIC_LETTERS)]
            ltr_tone = DiatonicFoundation.get_tone(ltr)
            for a in range(-2, 3):
                t = DiatonicTone.alter_tone_by_augmentation(ltr_tone, a)
                dist = t.placement - tone.placement if t.placement > tone.placement else t.placement - tone.placement + 12
                if dist == inc:
                    print(t)


if __name__ == "__main__":
    unittest.main()
