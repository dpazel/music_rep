import unittest
from tonalmodel.blues_modality import BluesModality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tests.utility import build_incremental_intervals
from tonalmodel.modality_factory import ModalityFactory


class TestBluesModality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_major_blues_key(self):
        blues_modality = BluesModality.create(ModalityType.MajorBlues)
        
        for key in blues_modality.get_valid_root_tones():
            scale = blues_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(blues_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == blues_modality.incremental_intervals
        print('End test_major_blues_key')
            
    def test_minor_blues_key(self):
        blues_modality = ModalityFactory.create_modality(ModalityType.MinorBlues)
        
        for key in blues_modality.get_valid_root_tones():
            scale = blues_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(blues_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == blues_modality.incremental_intervals
        print('End test_minor_blues_key')

    def test_print_blues(self):
        string_array = BluesModality.blues_modality_types_as_string_array()
        for s in string_array:
            print(s)
        assert len(string_array) == 2
