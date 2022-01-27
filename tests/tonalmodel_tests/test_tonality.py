import unittest
from tonalmodel.modality import Modality, ModalityType, ModalitySpec
from tonalmodel.tonality import Tonality
from tonalmodel.modality_factory import ModalityFactory

class TestTonality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_major_key(self):
        tonality = Tonality.create(ModalityType.Major, 'C', 0)

        assert ModalityType.Major == tonality.modality_type
        assert ModalityType.Major == tonality.modality.modality_type
        assert 0 == tonality.modal_index
        assert 'C' == tonality.diatonic_tone.diatonic_symbol
        assert ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'] == [t.diatonic_symbol for t in tonality.annotation]

    def test_major_modal_key(self):
        tonality = Tonality.create(ModalityType.Major, 'D', 1)

        assert ModalityType.Major == tonality.modality_type
        assert ModalityType.Major == tonality.modality.modality_type
        assert 1 == tonality.modal_index
        assert 'D' == tonality.diatonic_tone.diatonic_symbol
        assert 'C' == tonality.basis_tone.diatonic_symbol
        assert ['D', 'E', 'F', 'G', 'A', 'B', 'C', 'D'] == [t.diatonic_symbol for t in tonality.annotation]

    def test_build_on_basis(self):
        tonality = Tonality.create_on_basis_tone('E', ModalityType.Major, 1)

        assert 'E' == tonality.basis_tone.diatonic_symbol
        assert 'F#' == tonality.root_tone.diatonic_symbol

        tonality = Tonality.create_on_basis_tone('G', ModalityType.MelodicMinor, 2)

        assert 'G' == tonality.basis_tone.diatonic_symbol
        assert 'Bb' == tonality.root_tone.diatonic_symbol

    def test_build_user_defined_tonality(self):
        modality_type = ModalityType('my_modality')
        incremental_interval_strs = [
            'P:1', 'm:2', 'M:3', 'm:2', 'm:2', 'M:2', 'A:2'
        ]
        modality_spec = ModalitySpec(modality_type, incremental_interval_strs)
        modality = Modality(modality_spec)

        tonality = Tonality(modality, 'A')

        assert 0 == tonality.modal_index
        assert 'A' == tonality.diatonic_tone.diatonic_symbol
        assert ['A', 'Bb', 'D', 'Eb', 'Fb', 'Gb', 'A'] == [t.diatonic_symbol for t in tonality.annotation]

    def test_for_book(self):
        tonality_a = Tonality(ModalityFactory.create_modality(ModalityType.Major, 1), 'E')
        tonality_b = Tonality.create(ModalityType.Major, 'E', 1)
        tonality_c = Tonality.create_on_basis_tone('D', ModalityType.Major, 1)

        print('{0}:  [{1}]'.format(tonality_a, ','.join(tone.diatonic_symbol for tone in tonality_a.annotation)))
        print('{0}:  [{1}]'.format(tonality_b, ','.join(tone.diatonic_symbol for tone in tonality_b.annotation)))
        print('{0}:  [{1}]'.format(tonality_c, ','.join(tone.diatonic_symbol for tone in tonality_c.annotation)))

