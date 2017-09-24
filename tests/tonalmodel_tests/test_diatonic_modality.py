import unittest
from tonalmodel.diatonic_modality import DiatonicModality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tests.utility import build_incremental_intervals


class TestDiatonicModality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_major_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Major)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_major_key')
            
    def test_natural_minor_key(self):
        diatonic_modality = DiatonicModality(ModalityType.NaturalMinor)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_natural_minor_key')
        
    def test_melodic_minor_key(self):
        diatonic_modality = DiatonicModality(ModalityType.MelodicMinor)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_melodic_minor_key')
            
    def test_harmonic_minor_key(self):
        diatonic_modality = DiatonicModality(ModalityType.HarmonicMinor)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_harmonic_minor_key')
            
    def test_ionian_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Ionian)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_ionian_key')
            
    def test_dorian_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Dorian)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_dorian_key')
            
    def test_phrygian_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Phrygian)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_phrygian_key')
            
    def test_lydian_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Lydian)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_lydian_key')
            
    def test_Myxolydian_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Myxolydian)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_Myxolydian_key')
            
    def test_Aeolian_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Aeolian)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_Aeolian_key')
            
    def test_Locrian_key(self):
        diatonic_modality = DiatonicModality(ModalityType.Locrian)
        
        for key in diatonic_modality.get_valid_root_tones():
            scale = diatonic_modality.get_tonal_scale(DiatonicTone(key))
            print('{0} scale for {1} is [{2}]'.format(diatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale)))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == diatonic_modality.incremental_intervals
        print('End test_Locrian_key')
          
if __name__ == "__main__":
    unittest.main()
