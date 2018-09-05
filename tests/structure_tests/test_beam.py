import unittest

from structure.abstract_note import AbstractNote
from structure.beam import Beam
from structure.note import Note
from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.duration import Duration
from timemodel.offset import Offset


class NoteTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_beam(self):
        note = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        beam = Beam([note]) 
        print(beam)
        assert beam.cardinality() == 1
        assert beam.get_all_notes()[0].diatonic_pitch == DiatonicPitch(4, 'c')
        
        notes = beam.get_all_notes()
        assert len(notes) == 1
        NoteTest.print_all_notes(notes)
        
    def test_multi_notes(self):
        note0 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'd'), Duration(1, 8), 1)
        note2 = Note(DiatonicPitch(4, 'e'), Duration(1, 16))
        beam = Beam([note0, note1, note2]) 
        print(beam)
        assert beam.cardinality() == 3
        notes = beam.get_all_notes()
        assert notes[0].diatonic_pitch == DiatonicPitch(4, 'c')
        assert notes[1].diatonic_pitch == DiatonicPitch(4, 'd')
        assert notes[2].diatonic_pitch == DiatonicPitch(4, 'e')
        assert beam.duration == Duration(3, 8)
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(1, 8)
        assert notes[2].relative_position == Offset(5, 16)
              
        assert len(notes) == 3
        NoteTest.print_all_notes(notes)
        
    def test_nested_notes(self):        
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        note3 = Note(DiatonicPitch(4, 'e'), Duration(1, 16))
        sub_beam = Beam([note1, note2, note3]) 
        
        beam = Beam()
        beam.append(Note(DiatonicPitch(4, 'f'), Duration(1, 8)))
        beam.append(sub_beam)
        beam.append(Note(DiatonicPitch(4, 'g'), Duration(1, 8)))
        
        print(beam)
        
        notes = beam.get_all_notes()
        assert len(notes) == 5
        assert notes[0].diatonic_pitch == DiatonicPitch(4, 'f')
        assert notes[1].diatonic_pitch == DiatonicPitch(4, 'c')
        assert notes[2].diatonic_pitch == DiatonicPitch(4, 'd')
        assert notes[3].diatonic_pitch == DiatonicPitch(4, 'e')
        assert notes[4].diatonic_pitch == DiatonicPitch(4, 'g')
        
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(0)
        assert notes[2].relative_position == Offset(1, 16)
        assert notes[3].relative_position == Offset(1, 8)
        assert notes[4].relative_position == Offset(9, 32)
        NoteTest.print_all_notes(notes)

        notes = sub_beam.get_all_notes()
        NoteTest.print_all_notes(notes)

        b = Beam()
        b.append(beam)

        notes = sub_beam.get_all_notes()
        NoteTest.print_all_notes(notes)
        assert notes[0].duration == Duration(1, 32)
        assert str(notes[0].diatonic_pitch) == 'C:4'

        sub_beam_prime = sub_beam.clone()
        notes = sub_beam_prime.get_all_notes()
        NoteTest.print_all_notes(notes)
        assert notes[0].duration == Duration(1, 8)
        assert str(notes[0].diatonic_pitch) == 'C:4'

        beam_prime = beam.clone()
        notes = beam_prime.get_all_notes()
        NoteTest.print_all_notes(notes)
        assert notes[0].duration == Duration(1, 8)
        assert str(notes[0].diatonic_pitch) == 'F:4'

        b_prime = b.clone()
        notes = b_prime.get_all_notes()
        NoteTest.print_all_notes(notes)
        assert notes[0].duration == Duration(1, 16)
        assert str(notes[0].diatonic_pitch) == 'F:4'
        
    def test_insert_notes(self):
        print('test_insert_notes')
        # same as test_nested_notes
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        note3 = Note(DiatonicPitch(4, 'e'), Duration(1, 16))
        sub_beam = Beam([note1, note2, note3]) 
        
        beam = Beam()
        beam.append(Note(DiatonicPitch(4, 'f'), Duration(1, 8)))
        beam.append(sub_beam)
        beam.append(Note(DiatonicPitch(4, 'g'), Duration(1, 8))) 
        
        AbstractNote.print_structure(beam)
        
        # add a beam
        n_list = [Note(DiatonicPitch(3, 'c'), Duration(1, 8)), Note(DiatonicPitch(3, 'd'), Duration(1, 8))]
        add_beam = Beam(n_list)   
        sub_beam.add(add_beam, 1)  
        
        print(beam)
        AbstractNote.print_structure(beam)
        
        notes = beam.get_all_notes()
        assert len(notes) == 7
        NoteTest.print_all_notes(notes)
        assert notes[0].diatonic_pitch == DiatonicPitch(4, 'f')
        assert notes[1].diatonic_pitch == DiatonicPitch(4, 'c')
        assert notes[2].diatonic_pitch == DiatonicPitch(3, 'c')
        assert notes[3].diatonic_pitch == DiatonicPitch(3, 'd')
        assert notes[4].diatonic_pitch == DiatonicPitch(4, 'd')
        assert notes[5].diatonic_pitch == DiatonicPitch(4, 'e')
        assert notes[6].diatonic_pitch == DiatonicPitch(4, 'g')    
            
        assert notes[0].relative_position == Offset(0)
        assert notes[1].relative_position == Offset(0)
        assert notes[2].relative_position == Offset(0)
        assert notes[3].relative_position == Offset(1, 32)
        assert notes[4].relative_position == Offset(1, 8)
        assert notes[5].relative_position == Offset(3, 16)
        assert notes[6].relative_position == Offset(11, 32)
        
    def test_add_note_at_lower_level(self):
        print('start test_add_note_at_lower_level')
        sub_beam = Beam([Note(DiatonicPitch(2, 'c'), Duration(1, 8)), Note(DiatonicPitch(2, 'd'), Duration(1, 8))])
        beam = Beam([Note(DiatonicPitch(3, 'c'), Duration(1, 8)), sub_beam, Note(DiatonicPitch(3, 'd'),
                                                                                 Duration(1, 8))])
        
        AbstractNote.print_structure(beam)
        
        notes = beam.get_all_notes()
        assert len(notes) == 4
        
        assert beam.sub_notes[1].duration == Duration(1, 8)
        assert beam.sub_notes[1].relative_position == Offset(1, 8)
        assert beam.sub_notes[1].sub_notes[1].duration == Duration(1, 16)
        assert beam.sub_notes[1].sub_notes[1].relative_position == Offset(1, 16)
        
        sub_beam.add(Note(DiatonicPitch(2, 'c'), Duration(1, 8)), 1)
        AbstractNote.print_structure(beam)
        
        assert beam.sub_notes[1].duration == Duration(3, 16)
        assert beam.sub_notes[1].relative_position == Offset(1, 8)
        assert beam.sub_notes[1].sub_notes[1].duration == Duration(1, 16)
        assert beam.sub_notes[1].sub_notes[1].relative_position == Offset(1, 16)
        
    def test_tie_break(self):
        print('test tie break')
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(3, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(3, 'c'), Duration(1, 8))
        d = Note(DiatonicPitch(3, 'a'), Duration(1, 8))
        sub_beam = Beam([b, c])  
        
        beam = Beam([a, d])  
        a.tie() 
        assert a.is_tied_to
        assert d.is_tied_from
        
        beam.add(sub_beam, 1)
        
        assert not a.is_tied_to
        assert not d.is_tied_from

    def test_odd_structure(self):
        print('test odd structure')
        n1 = Note(DiatonicPitch(4, 'c'), Duration(1, 24))
        n2 = Note(DiatonicPitch(4, 'c'), Duration(1, 24))
        n3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))

        beam = Beam([n1, n2, n3])

        #AbstractNote.print_structure((beam))

        n1 = Note(DiatonicPitch(4, 'c'), Duration(1, 12))
        n2 = Note(DiatonicPitch(4, 'c'), Duration(1, 12))

        from structure.tuplet import Tuplet
        tuplet = Tuplet(Duration(1, 12), 1, [n1, n2])

        n3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))

        beam = Beam([tuplet, n3])
        AbstractNote.print_structure(beam)


    @staticmethod
    def print_all_notes(notes):
        print('----------')
        for n in notes:
            print('{0} at {1}'.format(n, n.relative_position))
        print('----------')
            

if __name__ == "__main__":
    unittest.main()
