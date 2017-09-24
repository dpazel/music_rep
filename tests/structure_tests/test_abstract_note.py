import unittest

from structure.note import Note
from structure.beam import Beam
from structure.tuplet import Tuplet
from structure.abstract_note import AbstractNote
from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.duration import Duration
from timemodel.offset import Offset
from timemodel.offset import Position


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_beam_reverse(self):
        print('test simple beam reverse')
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(3, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(3, 'c'), Duration(1, 8)) 
        d = Note(DiatonicPitch(3, 'd'), Duration(1, 8)) 
        beam = Beam([a, b, c, d]) 
        
        print(beam)
        
        beam.reverse()
        
        print(beam)
        
        notes = beam.get_all_notes()
        assert notes is not None
        assert len(notes) == 4
        assert notes[0].diatonic_pitch == DiatonicPitch(3, 'd')
        assert notes[1].diatonic_pitch == DiatonicPitch(3, 'c')
        assert notes[2].diatonic_pitch == DiatonicPitch(3, 'b')
        assert notes[3].diatonic_pitch == DiatonicPitch(3, 'a')
        
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(1, 8)
        assert notes[2].relative_position == Offset(1, 4)
        assert notes[3].relative_position == Offset(3, 8)
        
    def test_simple_tuplet_reverse(self):
        print('test simple tuplet reverse')
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(3, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(3, 'c'), Duration(1, 8)) 
        d = Note(DiatonicPitch(3, 'd'), Duration(1, 8)) 
        tuplet = Tuplet(Duration(1, 8), 3, [a, b, c, d]) 
        
        print(tuplet)
        
        tuplet.reverse()
        
        print(tuplet)
        
        notes = tuplet.get_all_notes()
        assert notes is not None
        assert len(notes) == 4
        assert notes[0].diatonic_pitch == DiatonicPitch(3, 'd')
        assert notes[1].diatonic_pitch == DiatonicPitch(3, 'c')
        assert notes[2].diatonic_pitch == DiatonicPitch(3, 'b')
        assert notes[3].diatonic_pitch == DiatonicPitch(3, 'a')
        
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(3, 32)
        assert notes[2].relative_position == Offset(3, 16)
        assert notes[3].relative_position == Offset(9, 32)
        
    def test_nested_structure_reverse(self):
        print('test nested structure reverse')
        a = Note(DiatonicPitch(4, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(4, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(4, 'c'), Duration(1, 8)) 
        d = Note(DiatonicPitch(4, 'd'), Duration(1, 8)) 
        tuplet = Tuplet(Duration(1, 8), 3, [a, b, c, d]) 
        
        e = Note(DiatonicPitch(4, 'e'), Duration(1, 8))  
        f = Note(DiatonicPitch(4, 'f'), Duration(1, 8)) 
        g = Note(DiatonicPitch(4, 'g'), Duration(1, 8)) 
        a1 = Note(DiatonicPitch(3, 'a'), Duration(1, 8)) 
        sub_beam = Beam([e, f, g, a1])  
        
        b1 = Note(DiatonicPitch(3, 'b'), Duration(1, 8))    
        c1 = Note(DiatonicPitch(3, 'c'), Duration(1, 8))  
        d1 = Note(DiatonicPitch(3, 'd'), Duration(1, 8))  
        e1 = Note(DiatonicPitch(3, 'e'), Duration(1, 8))  
        
        beam = Beam([b1, tuplet, c1, sub_beam, d1, e1])
        
        AbstractNote.print_structure(beam)
        
        beam.reverse()
        
        AbstractNote.print_structure(beam)
        
        notes = beam.get_all_notes()
        assert notes is not None
        assert len(notes) == 12
        
        assert notes[0].diatonic_pitch == DiatonicPitch(3, 'e')
        assert notes[1].diatonic_pitch == DiatonicPitch(3, 'd')
        assert notes[2].diatonic_pitch == DiatonicPitch(3, 'a')
        assert notes[3].diatonic_pitch == DiatonicPitch(4, 'g')
        assert notes[4].diatonic_pitch == DiatonicPitch(4, 'f')
        assert notes[5].diatonic_pitch == DiatonicPitch(4, 'e')
        assert notes[6].diatonic_pitch == DiatonicPitch(3, 'c')
        assert notes[7].diatonic_pitch == DiatonicPitch(4, 'd')
        assert notes[8].diatonic_pitch == DiatonicPitch(4, 'c')
        assert notes[9].diatonic_pitch == DiatonicPitch(4, 'b')
        assert notes[10].diatonic_pitch == DiatonicPitch(4, 'a')
        assert notes[11].diatonic_pitch == DiatonicPitch(3, 'b')
        
    def test_ties_reverse(self):
        print('test ties reverse')
        a = Note(DiatonicPitch(3, 'b'), Duration(1, 8))  
        b = Note(DiatonicPitch(4, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(4, 'c'), Duration(1, 8)) 
        d = Note(DiatonicPitch(4, 'd'), Duration(1, 8)) 
        tuplet = Tuplet(Duration(1, 8), 3, [a, b, c, d]) 
        
        e = Note(DiatonicPitch(4, 'd'), Duration(1, 8))  
        f = Note(DiatonicPitch(4, 'f'), Duration(1, 8)) 
        g = Note(DiatonicPitch(4, 'g'), Duration(1, 8)) 
        a1 = Note(DiatonicPitch(3, 'd'), Duration(1, 8)) 
        sub_beam = Beam([e, f, g, a1])  
        
        b1 = Note(DiatonicPitch(3, 'b'), Duration(1, 8))    
        c1 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))  
        d1 = Note(DiatonicPitch(3, 'd'), Duration(1, 8))  
        e1 = Note(DiatonicPitch(3, 'e'), Duration(1, 8))  
        
        beam = Beam([b1, tuplet, c1, sub_beam, d1, e1])
        
        b1.tie()
        d.tie()
        c1.tie()
        a1.tie()
        
        AbstractNote.print_structure(beam)
        
        beam.reverse()
        
        AbstractNote.print_structure(beam)
        
        assert a.is_tied_to and a.tied_to == b1 
        assert b1.is_tied_from and b1.tied_from == a

        assert c1.is_tied_to and c1.tied_to == d 
        assert d.is_tied_from and d.tied_from == c1
        
        assert e.is_tied_to and e.tied_to == c1 
        assert c1.is_tied_from and c1.tied_from == e
               
        assert d1.is_tied_to and d1.tied_to == a1 
        assert a1.is_tied_from and a1.tied_from == d1
        
    def test_absolute_position(self):
        print('test absolute position')
        
        a = Note(DiatonicPitch(4, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(4, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(4, 'c'), Duration(1, 8)) 
        d = Note(DiatonicPitch(4, 'd'), Duration(1, 8)) 
        tuplet = Tuplet(Duration(1, 8), 3, [a, b, c, d]) 
        
        e = Note(DiatonicPitch(4, 'e'), Duration(1, 8))  
        f = Note(DiatonicPitch(4, 'f'), Duration(1, 8)) 
        g = Note(DiatonicPitch(4, 'g'), Duration(1, 8)) 
        a1 = Note(DiatonicPitch(3, 'a'), Duration(1, 8)) 
        sub_beam = Beam([e, f, g, a1])  
        
        b1 = Note(DiatonicPitch(3, 'b'), Duration(1, 8))    
        c1 = Note(DiatonicPitch(3, 'c'), Duration(1, 8))  
        d1 = Note(DiatonicPitch(3, 'd'), Duration(1, 8))  
        e1 = Note(DiatonicPitch(3, 'e'), Duration(1, 8))  
        
        beam = Beam([b1, tuplet, c1, sub_beam, d1, e1])
        
        AbstractNote.print_structure(beam)
        
        notes = beam.get_all_notes()
        assert notes is not None
        assert len(notes) == 12
        
        results = [Position(0), Position(1, 8), Position(7, 32), Position(5, 16),
                   Position(13, 32), Position(1, 2), Position(5, 8), Position(11, 16),
                   Position(3, 4), Position(13, 16), Position(7, 8), Position(1)
                   ]
        index = 0
        for n in notes:
            print('{0} abs. position = {1}'.format(n, n.get_absolute_position()))
            assert n.get_absolute_position() == results[index]
            index += 1


if __name__ == "__main__":
    unittest.main()
