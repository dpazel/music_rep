import unittest

from structure.abstract_note import AbstractNote
from structure.beam import Beam
from structure.note import Note
from structure.line import Line

from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.position import Position

from timemodel.duration import Duration
from timemodel.offset import Offset

from instruments.instrument_catalog import InstrumentCatalog

from structure.voice import Voice
from structure.tuplet import Tuplet

from misc.interval import Interval


class TestVoice(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_single_voice(self):
        print('test single voice')
        note0 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'd'), Duration(1, 8), 1)
        note2 = Note(DiatonicPitch(4, 'e'), Duration(1, 16))
        beam = Beam([note0, note1, note2]) 
        print(beam)
        assert beam.cardinality() == 3
        
        line = Line(beam)
        
        assert line.length() == Duration(3, 8)
        
        c = InstrumentCatalog.instance()
        
        violin = c.get_instrument("violin")
        
        voice = Voice(violin)
        voice.pin(line, Offset(3, 4))
        
        coverage = voice.coverage()
        print('Coverage = {0}'.format(coverage))
        assert coverage.lower == Position(3, 4)
        assert coverage.upper == Position(9, 8)
        
        assert voice.length() == Duration(9, 8)
        
        interval = Interval(Position(15, 16), Position(9, 8))
        notes = voice.get_notes_by_interval(interval)
        print(', '.join([str(n) for n in notes]))
        for n in notes:
            intvl = TestVoice.compute_note_interval(n)
            print('{0} intersect {1} = {2}'.format(intvl, interval, intvl.intersection(interval)))
            
        assert len(notes) == 2
        print(notes[0].get_absolute_position(), notes[1].get_absolute_position())
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('D:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('E:4'))
        
    def test_two_voices(self):
        print('test two voices')
        c = InstrumentCatalog.instance()        
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        tuplet = Tuplet(Duration(1, 8), 2, [note0, note1, note2])
        
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        note4 = Note(DiatonicPitch(4, 'e'), Duration(1, 8)) 
        subbeam = Beam([note3, note4])  
        beam = Beam(subbeam)     
        line1 = Line([tuplet, beam])
        print(line1)
        
        notee0 = Note(DiatonicPitch(5, 'a'), Duration(1, 8))
        notee1 = Note(DiatonicPitch(5, 'b'), Duration(1, 8), 1)
        notee2 = Note(DiatonicPitch(5, 'c'), Duration(1, 8))     
        notee3 = Note(DiatonicPitch(5, 'd'), Duration(1, 16)) 
        line2 = Line([notee0, notee1, notee2])  
        line2.pin(notee3, Offset(1, 2)) 
        print(line2)
        
        voice = Voice(violin)
        voice.pin(line1, Offset(1, 4))
        voice.pin(line2, Offset(0, 1))
        
        print(voice)
        
        interval = Interval(Position(1, 2), Position(1))
        notes = voice.get_notes_by_interval(interval)
        
        assert len(notes) == 3
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('D:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('E:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('D:5'))
        
        interval = Interval(Position(1, 4), Position(7, 16))
        notes = voice.get_notes_by_interval(interval)
        
        assert len(notes) == 5
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:5'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:5'))
        
    def test_overlap_vs_start(self):
        c = InstrumentCatalog.instance()        
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
        
        line = Line()
        line.pin(note0, Offset(1, 4))
        line.pin(note1, Offset(3, 8))
        line.pin(note2, Offset(1, 2))
        line.pin(note3, Offset(5, 8))
        
        voice = Voice(violin)
        voice.pin(line, Offset(0))
        
        interval = Interval(Position(5, 16), Position(5, 8))
        
        notes = voice.get_notes_by_interval(interval)
        assert len(notes) == 3
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:4'))
        
        notes = voice.get_notes_starting_in_interval(interval)
        assert len(notes) == 2
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:4'))   
        
        notee0 = Note(DiatonicPitch(5, 'a'), Duration(1, 2))
        notee1 = Note(DiatonicPitch(5, 'b'), Duration(1, 2))  
        line1 = Line()
        line1.pin([notee0, notee1], Offset(0)) 
        
        voice.pin(line1, Offset(1, 4))  
        
        notes = voice.get_notes_by_interval(interval)
        assert len(notes) == 4
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:4'))   
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:5')) 
        
        notes = voice.get_notes_by_interval(interval, line1)  
        assert len(notes) == 1    
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:5'))   
        
        notes = voice.get_notes_starting_in_interval(interval)
        assert len(notes) == 2
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:4')) 
        
        notes = voice.get_notes_starting_in_interval(Interval(Position(1, 8), Position(3, 8)), line1)
        assert len(notes) == 1
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:5'))
        
    def test_remove_notes(self):
        c = InstrumentCatalog.instance()        
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
        
        line = Line()
        line.pin(note0, Offset(1, 4))
        line.pin(note1, Offset(3, 8))
        line.pin(note2, Offset(1, 2))
        line.pin(note3, Offset(5, 8))
        
        voice = Voice(violin)
        voice.pin(line, Offset(0))
        
        line.unpin([note1, note2])
        notes = voice.get_all_notes()
        assert len(notes) == 2
        assert note0 in notes
        assert note3 in notes
        assert note1 not in notes
        assert note2 not in notes
        
        notes = voice.get_notes_starting_in_interval(Interval(Position(0), Position(2, 1)))
        assert len(notes) == 2
        
        line.clear()
        notes = voice.get_all_notes()
        assert len(notes) == 0
        
        notes = voice.get_notes_starting_in_interval(Interval(Position(0), Position(2, 1)))
        assert len(notes) == 0
        
    def test_add_notes_to_line(self):
        c = InstrumentCatalog.instance()        
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
        
        line = Line()
        line.pin(note0, Offset(1, 4))
        line.pin(note1, Offset(3, 8))
        line.pin(note2, Offset(1, 2))
        line.pin(note3, Offset(5, 8))
        
        voice = Voice(violin)
        voice.pin(line, Offset(0))
        
        notee0 = Note(DiatonicPitch(5, 'a'), Duration(1, 8))
        notee1 = Note(DiatonicPitch(5, 'b'), Duration(1, 8))
        line.pin([notee0, notee1], Offset(3, 4))
        
        notes = voice.get_notes_starting_in_interval(Interval(Position(5, 8), Position(2, 1)))
        assert len(notes) == 3
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('D:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:5'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:5'))
        
    def test_add_notes_to_beam(self):
        c = InstrumentCatalog.instance()        
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
        beam = Beam([note2, note3])
        
        line = Line()
        line.pin(note0, Offset(1, 4))
        line.pin(note1, Offset(3, 8))
        line.pin(beam, Offset(1, 2))
        
        voice = Voice(violin)
        voice.pin(line, Offset(0))   
        
        notee0 = Note(DiatonicPitch(5, 'a'), Duration(1, 8))
        notee1 = Note(DiatonicPitch(5, 'b'), Duration(1, 8))  
        beam.append([notee0, notee1])
        
        print(voice)
        notes = voice.get_notes_starting_in_interval(Interval(Position(3, 4), Position(1, 1)))
        
        assert len(notes) == 2
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:5'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('B:5'))
        
        # Do the same but append a Beam to a line
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
             
        line = Line()
        line.pin(note0, Offset(1, 4))
        line.pin(note1, Offset(3, 8))
     
        voice = Voice(violin)
        voice.pin(line, Offset(0))   
        
        beam = Beam([note2, note3])
        line.pin(beam, Offset(1, 2))   
        
        print(voice)
        notes = voice.get_notes_starting_in_interval(Interval(Position(1, 2), Position(1, 1)))  
        
        assert len(notes) == 2
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('D:4'))
        
        # Do the same but append a Beam to a Beam
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
             
        line = Line()
        beam = Beam([note0, note1])
        line.pin(beam, Offset(1, 4))
     
        voice = Voice(violin)
        voice.pin(line, Offset(0))   
        
        beam1 = Beam([note2, note3])
        beam.append(beam1)  
        
        print(voice)
        notes = voice.get_notes_starting_in_interval(Interval(Position(1, 2), Position(1, 1)))  
        
        assert len(notes) == 2
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('C:4'))
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('D:4'))
        
        # try to add note out of range on violin.
        notex = Note(DiatonicPitch(7, 'b'), Duration(1, 8))
        with self.assertRaises(Exception):
            line.pin(notex, Offset(3, 1))
        
    def test_add_notes_to_tuplet(self):
        c = InstrumentCatalog.instance()        
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))   
        beam = Beam([note0, note1])
        
        line = Line()
        line.pin(beam, Offset(1, 2))
        
        voice = Voice(violin)
        voice.pin(line, Offset(0))   
        
        tuplet = Tuplet(Duration(1, 8), 3, [note2, note3])
        beam.append(tuplet)
        
        notee0 = Note(DiatonicPitch(5, 'a'), Duration(1, 8))
        tuplet.append(notee0)
        
        print(voice)
        notes = voice.get_notes_starting_in_interval(Interval(Position(1, 2), Position(5, 4)))
        
        assert len(notes) == 5
        assert TestVoice.has_pitch(notes, DiatonicPitch.parse('A:5'))

        beam_prime = beam.clone()
        notes = beam_prime.get_all_notes()
        AbstractNote.print_structure(beam_prime)
        assert notes[0].duration == Duration(1, 8)
        assert str(notes[0].diatonic_pitch) == 'A:4'

        line_prime = line.clone()
        notes = line_prime.get_all_notes()
        AbstractNote.print_structure(line_prime)
        assert notes[0].duration == Duration(1, 8)
        assert str(notes[0].diatonic_pitch) == 'A:4'
        assert notes[2].duration == Duration(1, 8)
        assert str(notes[2].diatonic_pitch) == 'C:4'

    @staticmethod
    def compute_note_interval(note):
        start = note.get_absolute_position()
        lenn = note.duration
        return Interval(start, start + lenn)
    
    @staticmethod
    def has_pitch(notes, pitch):
        for n in notes:
            if n.diatonic_pitch == pitch:
                return True
        return False
