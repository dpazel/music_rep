import unittest
from tonalmodel.diatonic_modality import DiatonicModality
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality

class TestTonality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_major_key(self):
        tonality = Tonality(ModalityType.Major, 'C', 0)

        assert ModalityType.Major == tonality.modality_type
        assert ModalityType(ModalityType.Major) == tonality.modality.modality_type
        assert 0 == tonality.modal_index
        assert 'C' == tonality.diatonic_tone.diatonic_symbol
        assert ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'] == [t.diatonic_symbol for t in tonality.annotation]

    def test_major_modal_key(self):
        tonality = Tonality(ModalityType.Major, 'D', 1)

        assert ModalityType.Major == tonality.modality_type
        assert ModalityType(ModalityType.Major) == tonality.modality.modality_type
        assert 1 == tonality.modal_index
        assert 'D' == tonality.diatonic_tone.diatonic_symbol
        assert 'C' == tonality.basis_tone.diatonic_symbol
        assert ['D', 'E', 'F', 'G', 'A', 'B', 'C', 'D'] == [t.diatonic_symbol for t in tonality.annotation]

    def test_build_on_basis(self):
        tonality = Tonality.create_on_basis_tone('E', ModalityType.Major, 1)

        assert 'E' == tonality.basis_tone.diatonic_symbol
        assert 'F#' == tonality.root_tone.diatonic_symbol