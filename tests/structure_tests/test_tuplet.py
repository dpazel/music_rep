import unittest
from structure.note import Note
from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.duration import Duration
from timemodel.offset import Offset
from structure.tuplet import Tuplet
from structure.beam import Beam
from structure.abstract_note import AbstractNote


class TestTuplet(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_tuplet(self):
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        note3 = Note(DiatonicPitch(4, 'e'), Duration(1, 8))
        tuplet = Tuplet(Duration(1, 8), 2, [note1, note2, note3]) 
        
        print(tuplet)
        AbstractNote.print_structure(tuplet)
        
        notes = tuplet.get_all_notes()
        assert len(notes) == 3

        assert notes[0].diatonic_pitch == DiatonicPitch(4, 'c')
        assert notes[1].diatonic_pitch == DiatonicPitch(4, 'd')
        assert notes[2].diatonic_pitch == DiatonicPitch(4, 'e')
        assert notes[0].duration == Duration(1, 12)
        assert notes[1].duration == Duration(1, 12)
        assert notes[2].duration == Duration(1, 12)
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(1, 12)
        assert notes[2].relative_position == Offset(1, 6)
        
    def test_nested_tuplet(self):
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        sub_tuplet = Tuplet(Duration(1, 8), 2, [Note(DiatonicPitch(3, 'c'), Duration(1, 8)),
                                                Note(DiatonicPitch(3, 'd'), Duration(1, 8)),
                                                Note(DiatonicPitch(3, 'e'), Duration(1, 8))])
        tuplet = Tuplet(Duration(1, 8), 2, [note1, sub_tuplet, note2]) 
        
        print(tuplet)
        AbstractNote.print_structure(tuplet)
        
        notes = tuplet.get_all_notes()
        assert len(notes) == 5
        
        assert notes[0].duration == Duration(1, 16)
        assert notes[1].duration == Duration(1, 24)
        assert notes[2].duration == Duration(1, 24)
        assert notes[3].duration == Duration(1, 24)
        assert notes[4].duration == Duration(1, 16)
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(0)
        assert notes[2].relative_position == Offset(1, 24)
        assert notes[3].relative_position == Offset(1, 12)
        assert notes[4].relative_position == Offset(3, 16)
        
        assert tuplet.sub_notes[1].duration == Duration(1, 8)
        assert tuplet.sub_notes[1].relative_position == Offset(1, 16)

        sub_tuplet_prime = sub_tuplet.clone()
        notes = sub_tuplet_prime.get_all_notes()
        AbstractNote.print_structure(sub_tuplet_prime)
        assert notes[0].duration == Duration(1, 12)
        assert str(notes[0].diatonic_pitch) == 'C:3'

        tuplet_prime = tuplet.clone()
        notes = tuplet_prime.get_all_notes()
        AbstractNote.print_structure(tuplet_prime)
        assert notes[0].duration == Duration(1, 16)
        assert str(notes[0].diatonic_pitch) == 'C:4'
        assert notes[1].duration == Duration(1, 24)
        
    def test_tuplet_with_nested_beam(self):
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8)) 
        
        n_list = [Note(DiatonicPitch(3, 'c'), Duration(1, 8)), Note(DiatonicPitch(3, 'd'), Duration(1, 8))]
        add_beam = Beam(n_list) 
        
        tuplet = Tuplet(Duration(1, 8), 2, [note1, add_beam, note2])

        print(tuplet)
        AbstractNote.print_structure(tuplet)
        
        notes = tuplet.get_all_notes()
        assert len(notes) == 4
        
        assert tuplet.sub_notes[0].duration == Duration(1, 16)
        assert tuplet.sub_notes[0].relative_position == Offset(0)
        assert tuplet.sub_notes[1].duration == Duration(1, 8)
        assert tuplet.sub_notes[1].relative_position == Offset(1, 16)
        assert tuplet.sub_notes[2].duration == Duration(1, 16)
        assert tuplet.sub_notes[2].relative_position == Offset(3, 16)
        assert notes[1].duration == Duration(1, 16)
        assert notes[1].relative_position == Offset(0)
        assert notes[2].duration == Duration(1, 16)
        assert notes[2].relative_position == Offset(1, 16)

        add_beam_prime = add_beam.clone()
        notes = add_beam_prime.get_all_notes()
        AbstractNote.print_structure(add_beam_prime)
        assert notes[0].duration == Duration(1, 8)
        assert str(notes[0].diatonic_pitch) == 'C:3'

        tuplet_prime = tuplet.clone()
        notes = tuplet_prime.get_all_notes()
        AbstractNote.print_structure(tuplet_prime)
        assert notes[0].duration == Duration(1, 16)
        assert str(notes[0].diatonic_pitch) == 'C:4'
        assert notes[1].duration == Duration(1, 16)
        
    def test_TBB_layers(self):
        print('start test_TBB_layers')
        sub_sub_beam = Beam([Note(DiatonicPitch(2, 'c'), Duration(1, 8)), Note(DiatonicPitch(2, 'd'), Duration(1, 8))])
        sub_beam = Beam([Note(DiatonicPitch(3, 'c'), Duration(1, 8)), sub_sub_beam, Note(DiatonicPitch(3, 'd'),
                                                                                         Duration(1, 8))])
        
        AbstractNote.print_structure(sub_beam)
        
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
        print('-----------')
        tuplet = Tuplet(Duration(1, 8), 2, [note1, sub_beam, note2]) 
        AbstractNote.print_structure(tuplet)
        
        notes = tuplet.get_all_notes()
        assert len(notes) == 6
        
        assert tuplet.sub_notes[1].duration == Duration(3, 20)
        assert tuplet.sub_notes[1].relative_position == Offset(1, 20)
        assert tuplet.sub_notes[1].sub_notes[1].duration == Duration(1, 20)
        assert tuplet.sub_notes[1].sub_notes[1].relative_position == Offset(1, 20)
        
        sub_sub_beam.add(Note(DiatonicPitch(2, 'c'), Duration(1, 8)), 1)
        AbstractNote.print_structure(tuplet)
        
        assert tuplet.sub_notes[1].duration == Duration(7, 44)
        assert tuplet.sub_notes[1].relative_position == Offset(1, 22)
        assert tuplet.sub_notes[1].sub_notes[1].duration == Duration(3, 44)
        assert tuplet.sub_notes[1].sub_notes[1].relative_position == Offset(1, 22)
        
        print('end test_TBB_layers')
        
    def test_tuplet_variations(self):
        print('test tuplet variations')
             
        # 1. Beam with 3 1/8 notes
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))  
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        beam = Beam([note1, note2, note3])    
        AbstractNote.print_structure(beam)    
        
        notes = beam.get_all_notes()
        assert len(notes) == 3  
        assert notes[0].duration == Duration(1, 8)
        assert notes[1].duration == Duration(1, 8)
        assert notes[2].duration == Duration(1, 8)
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(1, 8)
        assert notes[2].relative_position == Offset(1, 4) 
        
        # 2. beam with a tuplet
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))  
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        tuplet = Tuplet(Duration(1, 8), 2, [note1, note2, note3])  
        beam = Beam([tuplet])  
        AbstractNote.print_structure(beam)    
        
        notes = beam.get_all_notes()
        assert len(notes) == 3  
        assert notes[0].duration == Duration(1, 12)
        assert notes[1].duration == Duration(1, 12)
        assert notes[2].duration == Duration(1, 12)
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(1, 12)
        assert notes[2].relative_position == Offset(1, 6)          
        
        # 3. tuplet with a beam
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))  
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        beam = Beam([note1, note2, note3])  
        tuplet = Tuplet(Duration(1, 8), 2, beam)  
        AbstractNote.print_structure(tuplet)  
        
        notes = beam.get_all_notes()
        assert len(notes) == 3  
        
        assert notes[0].duration == Duration(1, 12)
        assert notes[1].duration == Duration(1, 12)
        assert notes[2].duration == Duration(1, 12)
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(1, 12)
        assert notes[2].relative_position == Offset(1, 6) 
        
        # 4. beam a beam of a tuplet
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))  
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        tuplet = Tuplet(Duration(1, 8), 2, [note1, note2, note3])  
        sub_beam = Beam([tuplet]) 
        beam = Beam(sub_beam) 
        AbstractNote.print_structure(beam) 
        
        notes = beam.get_all_notes()
        assert len(notes) == 3  
        
        assert notes[0].duration == Duration(1, 24)
        assert notes[1].duration == Duration(1, 24)
        assert notes[2].duration == Duration(1, 24)
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(1, 24)
        assert notes[2].relative_position == Offset(1, 12)   
        
    def test_tie_break(self):
        print('test tie break')
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(3, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(3, 'c'), Duration(1, 8))
        d = Note(DiatonicPitch(3, 'a'), Duration(1, 8))
        sub_beam = Beam([b, c])  
        
        tuplet = Tuplet(Duration(1, 8), 2, [a, d])  
        a.tie() 
        assert a.is_tied_to
        assert d.is_tied_from
        
        tuplet.add(sub_beam, 1)
        
        assert not a.is_tied_to
        assert not d.is_tied_from
        
    def test_dilation(self):
        print('test dilation')
        
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(3, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(3, 'c'), Duration(1, 8))
        d = Note(DiatonicPitch(3, 'd'), Duration(1, 8))
        e = Note(DiatonicPitch(3, 'e'), Duration(1, 8))

        tuplet = Tuplet(Duration(1, 8), 2, [a, b, c])    
        sub_beam = Beam([tuplet]) 
        
        beam = Beam([d, sub_beam, e])
        
        AbstractNote.print_structure(beam)   
        
        f = Note(DiatonicPitch(3, 'f'), Duration(1, 8))
        tuplet.add(f, 2)
        
        AbstractNote.print_structure(beam) 
        
        print('end test dilation')

    def test_book_example(self):
        print("test_book_example")
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))
        b = Note(DiatonicPitch(3, 'b'), Duration(1, 8))
        c = Note(DiatonicPitch(3, 'c'), Duration(1, 8))
        d = Note(DiatonicPitch(3, 'd'), Duration(1, 8))
        e = Note(DiatonicPitch(3, 'e'), Duration(1, 8))

        tuplet = Tuplet(Duration(1, 8), 2, [b, c, d])

        beam = Beam([a, tuplet, e])
        print(beam)

        a1 = Note(DiatonicPitch(3, 'a'), Duration(1, 8))
        b1 = Note(DiatonicPitch(3, 'b'), Duration(1, 8))
        c1 = Note(DiatonicPitch(3, 'c'), Duration(1, 8))
        d1 = Note(DiatonicPitch(3, 'd'), Duration(1, 8))
        e1 = Note(DiatonicPitch(3, 'e'), Duration(1, 8))

        tuplet1 = Tuplet(Duration(1, 8), 2, [b1, c1, d1])

        beam1 = Beam([tuplet1])

        final_beam = Beam([a1, beam1, e1])

        print(final_beam)

        a2 = Note(DiatonicPitch(3, 'a'), Duration(1, 8))
        b2 = Note(DiatonicPitch(3, 'b'), Duration(1, 8))
        c2 = Note(DiatonicPitch(3, 'c'), Duration(1, 8))
        d2 = Note(DiatonicPitch(3, 'd'), Duration(1, 8))
        e2 = Note(DiatonicPitch(3, 'e'), Duration(1, 8))

        beam2 = Beam([b2, c2, d2])
        tuplet2 = Tuplet(Duration(1, 16), 2, [beam2])
        final_beam2 = Beam([a2, tuplet2, e2])

        print(final_beam2)

        print("end test_book_example")
