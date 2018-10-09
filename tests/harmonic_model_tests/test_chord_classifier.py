import unittest
from harmonicmodel.chord_classifier import ChordClassifier

from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.diatonic_tone import DiatonicTone


class TestChordClassifier(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_tertian(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_list = ChordClassifier.classify(['e', 'a', 'c', 'g', 'B'], 'a', diatonic_tonality)

        assert 2 == len(chord_list)

        TestChordClassifier.print_chord_list('test_simple_tertian', chord_list)

        chord_list = ChordClassifier.classify(['e', 'a', 'c', 'g', 'B'], 'a')
        TestChordClassifier.print_chord_list('test_simple_tertian', chord_list)

        assert 2 == len(chord_list)

    def test_simple_quartal(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_list = ChordClassifier.classify(['e', 'a', 'd'], 'e', diatonic_tonality)
        assert 1 == len(chord_list)
        assert "PerPer" == str(chord_list[0].chord_type)

        TestChordClassifier.print_chord_list('test_simple_quartal', chord_list)

        chord_list = ChordClassifier.classify(['e', 'a', 'd', 'Bb'], 'e', diatonic_tonality)
        assert 0 == len(chord_list)

    def test_simple_secundal(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_list = ChordClassifier.classify(['d', 'c', 'e'], 'c', diatonic_tonality)
        assert 1 == len(chord_list)
        assert "MajMaj" == str(chord_list[0].chord_type)

        TestChordClassifier.print_chord_list('test_simple_secundal', chord_list)

        chord_list = ChordClassifier.classify(['d', 'c', 'e', 'f'], 'c', diatonic_tonality)

        TestChordClassifier.print_chord_list('test_simple_secundal', chord_list)
        assert 0 == len(chord_list)

    def test_simple_all_chords(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_list = ChordClassifier.classify_all_roots(['e', 'a', 'c', 'g', 'B'], diatonic_tonality)

        TestChordClassifier.print_chord_list('test_simple_all_chords', chord_list)

    @staticmethod
    def print_chord_list(header, chord_list):
        print(header)

        if chord_list is None:
            print("No chords found")
        else:
            for chord in chord_list:
                print('result is \'{0}\'.'.format(chord))
