import unittest
from tonalmodel.whole_tone_modality import WholeToneModality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tests.utility import build_incremental_intervals


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_whole_tone_key(self):
        whole_tone_modality = WholeToneModality(ModalityType.WholeTone)
        
        for key in whole_tone_modality.get_valid_root_tones():
            scale = whole_tone_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(whole_tone_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == whole_tone_modality.incremental_intervals
        print('End test_whole_tone_key')

if __name__ == "__main__":
    unittest.main()
