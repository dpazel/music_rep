import unittest

from tonalmodel.modality_factory import ModalityFactory
from tonalmodel.modality import ModalityType, ModalitySpec
from tonalmodel.diatonic_foundation import DiatonicFoundation


class TestPentatonicModality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_book_examples(self):
        modality = ModalityFactory.create_modality(ModalityType.Major)
        assert modality is not None

        modality = ModalityFactory.create_modality(ModalityType.MajorPentatonic, 1)
        assert modality is not None

        my_modality = 'my_modality'
        modality_type = ModalityType(my_modality)
        incremental_interval_strs = [
            'P:1', 'm:2', 'M:3', 'm:2', 'm:2', 'M:2', 'A:2'
        ]
        modality_spec = ModalitySpec(modality_type, incremental_interval_strs)
        ModalityFactory.register_modality(modality_type, modality_spec)
        modality = ModalityFactory.create_modality(ModalityType(my_modality))
        assert modality is not None

        tones = modality.get_tonal_scale(DiatonicFoundation.get_tone('Eb'))
        print('[{0}]'.format(','.join(str(tone.diatonic_symbol) for tone in tones)))
