import unittest

from tonalmodel.modality_factory import ModalityFactory
from tonalmodel.octatonic_modality import OctatonicModality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tests.utility import build_incremental_intervals


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_HW_Octatonic_key(self):
        octatonic_modality = OctatonicModality.create(ModalityType.HWOctatonic)
        
        for key in octatonic_modality.get_valid_root_tones():
            scale = octatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(octatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == octatonic_modality.incremental_intervals
        print('End test_HWOctatonic_key')
            
    def test_WH_Octatonic_key(self):
        octatonic_modality = ModalityFactory.create_modality(ModalityType.WHOctatonic)
        
        for key in octatonic_modality.get_valid_root_tones():
            scale = octatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(octatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == octatonic_modality.incremental_intervals
        print('End test_WHOctatonic_key')
