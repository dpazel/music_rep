import unittest
from structure.note import Note
from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.duration import Duration
from structure.beam import Beam


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_construction(self):
        note = Note(DiatonicPitch(4, 'c'), Duration(1, 4))
        print(note)
        assert note.base_duration == Duration(1, 4)
        assert note.duration == Duration(1, 4)
        assert str(note.diatonic_pitch) == 'C:4'
        assert not note.is_rest
        
        # quarter rest
        note = Note(None, Duration(1, 4))
        print(note)
        assert note.base_duration == Duration(1, 4)
        assert note.duration == Duration(1, 4)
        assert note.diatonic_pitch is None
        assert note.is_rest
        
        note = Note(DiatonicPitch(4, 'c'), Duration(1, 4), 2)
        print(note)
        assert note.base_duration == Duration(1, 4)
        assert note.duration == Duration(7, 16)
        assert str(note.diatonic_pitch) == 'C:4'
        assert not note.is_rest

        note = Note(DiatonicPitch(5, 'f#'), 'Q', 2)
        print(note)
        assert note.base_duration == Duration(1, 4)
        assert note.duration == Duration(7, 16)
        assert str(note.diatonic_pitch) == 'F#:5'
        assert not note.is_rest
        
    def test_next_prior_note(self):
        print('test_next_note')
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(3, 'b'), Duration(1, 8)) 
        c = Note(DiatonicPitch(4, 'c'), Duration(1, 8)) 
        d = Note(DiatonicPitch(4, 'd'), Duration(1, 8)) 
        e = Note(DiatonicPitch(4, 'e'), Duration(1, 8)) 
        f = Note(DiatonicPitch(4, 'f'), Duration(1, 8)) 
        g = Note(DiatonicPitch(4, 'g'), Duration(1, 8))  
        h = Note(DiatonicPitch(4, 'a'), Duration(1, 8))   
        full_list = [a, b, c, d, e, f, g, h]

        b3 = Beam([d, e])
        b2 = Beam([c, b3, f])
        b1 = Beam([b, b2, g])
        Beam([a, b1, h])
        
        print('next note test')
        n = a
        index = 1
        while True:
            n = n.next_note()
            if n is None:
                break
            print(n)
            assert n.diatonic_pitch == full_list[index].diatonic_pitch
            index += 1
        
        print('prior note test')
        n = h
        print(n)
        index = len(full_list) - 2
        while True:
            n = n.prior_note()
            if n is None:
                break
            print(n)
            assert n.diatonic_pitch == full_list[index].diatonic_pitch
            index -= 1
            
    def test_tie(self):
        print('test_next_note')
        a = Note(DiatonicPitch(3, 'a'), Duration(1, 8))  
        b = Note(DiatonicPitch(3, 'a'), Duration(1, 8)) 
        c = Note(DiatonicPitch(3, 'c'), Duration(1, 8))
        Beam([a, b, c])
        
        assert not a.is_tied_to
        assert not b.is_tied_from
        
        a.tie()
        assert a.is_tied_to
        assert b.is_tied_from
        assert a.tied_to == b
        assert b.tied_from == a
        
        a.untie()
        assert not a.is_tied_to
        assert not b.is_tied_from
        assert a.tied_to is None
        assert b.tied_from is None
        
        with self.assertRaises(Exception):
            c.tie()

if __name__ == "__main__":
    unittest.main()
