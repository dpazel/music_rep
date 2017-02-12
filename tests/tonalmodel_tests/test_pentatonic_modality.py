import unittest
from tonalmodel.pentatonic_modality import PentatonicModality
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tests.utility import build_incremental_intervals


class TestPentatonicModality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pentatonic_major_key(self):
        pentatonic_modality = PentatonicModality(ModalityType.MajorPentatonic)
        
        for key in pentatonic_modality.get_valid_root_tones():
            scale = pentatonic_modality.get_tonal_scale(DiatonicTone(key))
            print '{0} scale for {1} is [{2}]'.format(pentatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == pentatonic_modality.incremental_intervals
        print 'End test_pentatonic_major_key'

    def test_pentatonic_egyptian_key(self):
        pentatonic_modality = PentatonicModality(ModalityType.EgyptianPentatonic)
        
        for key in pentatonic_modality.get_valid_root_tones():
            scale = pentatonic_modality.get_tonal_scale(DiatonicTone(key))
            print '{0} scale for {1} is [{2}]'.format(pentatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == pentatonic_modality.incremental_intervals
        print 'End test_pentatonic_egyption_key'
            
    def test_pentatonic_minor_blues_key(self):
        pentatonic_modality = PentatonicModality(ModalityType.MinorBluesPentatonic)
        
        for key in pentatonic_modality.get_valid_root_tones():
            scale = pentatonic_modality.get_tonal_scale(DiatonicTone(key))
            print '{0} scale for {1} is [{2}]'.format(pentatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == pentatonic_modality.incremental_intervals
        print 'End test_pentatonic_minor_blues_key'
            
    def test_pentatonic_major_blues_key(self):
        pentatonic_modality = PentatonicModality(ModalityType.MajorBluesPentatonic)
        
        for key in pentatonic_modality.get_valid_root_tones():
            scale = pentatonic_modality.get_tonal_scale(DiatonicTone(key))
            print '{0} scale for {1} is [{2}]'.format(pentatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == pentatonic_modality.incremental_intervals
        print 'End test_pentatonic_major_blues_key'
            
    def test_pentatonic_minor_key(self):
        pentatonic_modality = PentatonicModality(ModalityType.MinorPentatonic)
        
        for key in pentatonic_modality.get_valid_root_tones():
            scale = pentatonic_modality.get_tonal_scale(DiatonicTone(key))
            print '{0} scale for {1} is [{2}]'.format(pentatonic_modality.get_modality_name, key,
                                                      ', '.join(dt.diatonic_symbol for dt in scale))
            
            incremental_intervals = build_incremental_intervals(scale)           
            assert incremental_intervals == pentatonic_modality.incremental_intervals
        print 'End test_pentatonic_minor_key'

if __name__ == "__main__":
    unittest.main()
