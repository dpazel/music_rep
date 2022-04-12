import unittest

from structure.tempo import Tempo, TempoType
from fractions import Fraction
from timemodel.duration import Duration


class TempoTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tempo_type(self):
        ty = TempoType.Grave
        print(str(ty))
        print(ty.get_range())
        self.assertTrue(str(ty) == 'Grave')
        self.assertTrue(ty.get_range().start_index == 25)
        self.assertTrue(ty.get_range().end_index == 45)
        
        ty = TempoType.Lento
        print(ty)
        print(ty.get_range())
        self.assertTrue(str(ty) == 'Lento')
        self.assertTrue(ty.get_range().start_index == 45)
        self.assertTrue(ty.get_range().end_index == 60)
        
        r = TempoType.get_range_for(TempoType.Adagio)
        self.assertTrue(r.start_index == 66)
        self.assertTrue(r.end_index == 76)
        
        r = TempoType.get_range_for(TempoType(TempoType.Adagio))
        self.assertTrue(r.start_index == 66)
        self.assertTrue(r.end_index == 76)
        
        tlist = TempoType.get_types()
        self.assertTrue(len(tlist) > 0)
        
    def test_tempo(self):
        tempo = Tempo(34)
        self.assertTrue(tempo.tempo == 34)
        
        tempo = Tempo(TempoType.Adagio)
        r = TempoType.get_range_for(TempoType.Adagio)
        self.assertTrue(r.end_index >= tempo.tempo >= r.start_index)
        
    def test_translate(self):
        tempo = Tempo(50)
        self.assertTrue(tempo.beat_duration.duration == Fraction(1, 4))
        translate = tempo.effective_tempo(Duration(1, 2))
        print(translate)
        self.assertTrue(translate == 25)
        
        translate = tempo.effective_tempo(Duration(1, 8))
        print(translate)
        self.assertTrue(translate == 100)
        
        tempo = Tempo(50, Duration(3, 8))
        self.assertTrue(tempo.beat_duration.duration == Fraction(3, 8))
        translate = tempo.effective_tempo(Duration(1, 8))
        print(translate)
        self.assertTrue(translate == 150)
        
        tempo = Tempo(30.5)
        self.assertTrue(tempo.tempo == 30.5)
        self.assertTrue(tempo.beat_duration.duration == Fraction(1, 4))
        translate = tempo.effective_tempo(Duration(1, 2))
        print(translate)
        self.assertTrue(translate == 15.25)
        translate = tempo.effective_tempo(Duration(1, 8))
        print(translate)
        self.assertTrue(translate == 61)

        tempo = Tempo(TempoType.Adagio, Duration(1, 4))
        print(tempo)
