import unittest
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_pitch import DiatonicPitch


class DiatonicFoundationTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_map_to_diatonic_scale(self):
        answers = DiatonicFoundation.map_to_diatonic_scale(46)
            
        assert DiatonicPitch.parse('Cbb:4') in answers
        assert DiatonicPitch.parse('A#:3') in answers
        assert DiatonicPitch.parse('Bb:3') in answers
        answers = DiatonicFoundation.map_to_diatonic_scale(47)
            
        assert DiatonicPitch.parse('Cb:4') in answers
        assert DiatonicPitch.parse('A##:3') in answers
        assert DiatonicPitch.parse('B:3') in answers
            
        answers = DiatonicFoundation.map_to_diatonic_scale(48)
            
        assert DiatonicPitch.parse('C:4') in answers
        assert DiatonicPitch.parse('B#:3') in answers
        assert DiatonicPitch.parse('Dbb:4') in answers
        
        answers = DiatonicFoundation.map_to_diatonic_scale(49)        
            
        assert DiatonicPitch.parse('C#:4') in answers
        assert DiatonicPitch.parse('B##:3') in answers
        assert DiatonicPitch.parse('Db:4') in answers
        
    def test_get_tones(self):
        tones = DiatonicFoundation.get_tones()
        
        assert tones is not None
        assert len(tones) > 12
        print len(tones)
        
    def test_semitone_difference(self):
        assert DiatonicFoundation.get_chromatic_distance(DiatonicPitch.parse('C:4')) == 48
        
        equi_list = DiatonicFoundation.add_semitones(DiatonicPitch.parse('eb:4'), 13)
        assert equi_list is not None
        assert len(equi_list) == 3
        assert DiatonicPitch.parse('E:5') in equi_list
        assert DiatonicPitch.parse('D##:5') in equi_list
        assert DiatonicPitch.parse('Fb:5') in equi_list
               
        a = DiatonicPitch.parse('C:5')
        b = DiatonicPitch.parse('F#:4')
        
        assert DiatonicFoundation.semitone_difference(a, b) == 6
        assert DiatonicFoundation.semitone_difference(b, a) == -6

if __name__ == "__main__":
    unittest.main()
