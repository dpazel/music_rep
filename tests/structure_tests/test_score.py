import unittest
from instruments.instrument_catalog import InstrumentCatalog
from structure.score import Score
from structure.instrument_voice import InstrumentVoice
from structure.line import Line
from structure.note import Note
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.position import Position
from misc.interval import Interval

from timemodel.time_signature_event import TimeSignatureEvent
from structure.time_signature import TimeSignature
from timemodel.tempo_event import TempoEvent
from structure.tempo import Tempo

from timemodel.beat_position import BeatPosition


class TestScore(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_setup(self):
        c = InstrumentCatalog.instance()   
        
        score = Score()
             
        violin = c.get_instrument("violin")
        violin_instrument_voice = InstrumentVoice(violin, 5)
        score.add_instrument_voice(violin_instrument_voice)
        
        trumpet = c.get_instrument("trumpet")
        trumpet_instrument_voice = InstrumentVoice(trumpet)
        score.add_instrument_voice(trumpet_instrument_voice)
        
        clarinet = c.get_instrument("clarinet")
        clarinet_instrument_voice = InstrumentVoice(clarinet)
        score.add_instrument_voice(clarinet_instrument_voice)
        
        voices = score.instrument_voices
        assert len(voices) == 3
        
        classes = score.instrument_classes
        assert len(classes) == 3
        
        assert TestScore.has_class(classes, 'strings')
        assert TestScore.has_class(classes, 'woodwinds')
        assert TestScore.has_class(classes, 'brass')
        
        score.remove_instrument_voice(trumpet_instrument_voice)
        classes = score.instrument_classes
        assert len(classes) == 2
        assert TestScore.has_class(classes, 'strings')
        assert TestScore.has_class(classes, 'woodwinds')
        
    def test_acquire_notes(self):
        c = InstrumentCatalog.instance()   
        
        score = Score()
            
        violin = c.get_instrument("violin")
        violin_instrument_voice = InstrumentVoice(violin)
        violin_voice = violin_instrument_voice.voice(0)
        assert violin_voice
        score.add_instrument_voice(violin_instrument_voice)
        
        clarinet = c.get_instrument("clarinet")
        clarinet_instrument_voice = InstrumentVoice(clarinet)
        clarinet_voice = clarinet_instrument_voice.voice(0)
        assert clarinet_voice
        score.add_instrument_voice(clarinet_instrument_voice)
        
        # Add notes to the score
        vnote0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        vnote1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        vnote2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))     
        vnote3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8)) 
        vnote4 = Note(DiatonicPitch(4, 'e'), Duration(1, 8))     
        vnote5 = Note(DiatonicPitch(4, 'f'), Duration(1, 8))   
        
        # Set up a violin voice with 6 8th notes 
        vline = Line([vnote0, vnote1, vnote2, vnote3, vnote4, vnote5])
        violin_voice.pin(vline)
        
        cnote0 = Note(DiatonicPitch(5, 'a'), Duration(1, 4))
        cnote1 = Note(DiatonicPitch(5, 'b'), Duration(1, 4))
        cnote2 = Note(DiatonicPitch(5, 'c'), Duration(1, 4))     
        cnote3 = Note(DiatonicPitch(5, 'd'), Duration(1, 4)) 
        
        # set up a clarinet line with 4 1`/4 notes
        cline = Line([cnote0, cnote1, cnote2, cnote3])
        clarinet_voice.pin(cline)
        
        # search for notes sounding in [1/4, 3/4)
        voice_note_map = score.get_notes_by_wnt_interval(Interval(Position(1, 4), Position(3, 4)))
        assert voice_note_map
        for (k, v) in voice_note_map.items():
            print k
            for (k1, v1) in v.items():
                print '{0} --> [{1}]'.format(k1, ', '.join(str(n) for n in v1))
                
        cvoice_map = voice_note_map.get(clarinet_instrument_voice)
        cvoices = cvoice_map.keys()
        assert cvoice_map
        assert cvoices[0] in cvoice_map
        cnotes = cvoice_map[cvoices[0]]
        assert len(cnotes) == 2
        assert TestScore.has_pitch(cnotes, DiatonicPitch.parse('B:5'))
        assert TestScore.has_pitch(cnotes, DiatonicPitch.parse('C:5'))
        
        vvoice_map = voice_note_map.get(violin_instrument_voice)
        vvoices = vvoice_map.keys()
        assert vvoice_map
        assert vvoices[0] in vvoice_map
        vnotes = vvoice_map[vvoices[0]]
        assert len(vnotes) == 4
        assert TestScore.has_pitch(vnotes, DiatonicPitch.parse('C:4'))
        assert TestScore.has_pitch(vnotes, DiatonicPitch.parse('F:4'))
        
        # search for notes starting in [3/8, 3/4)
        voice_note_map = score.get_notes_starting_in_wnt_interval(Interval(Position(3, 8), Position(3, 4)))
        assert voice_note_map
        for (k, v) in voice_note_map.items():
            print k
            for (k1, v1) in v.items():
                print '{0} --> [{1}]'.format(k1, ', '.join(str(n) for n in v1))
                
        cvoice_map = voice_note_map.get(clarinet_instrument_voice)
        cvoices = cvoice_map.keys()
        assert cvoice_map
        assert cvoices[0] in cvoice_map
        cnotes = cvoice_map[cvoices[0]]
        assert len(cnotes) == 1
        assert TestScore.has_pitch(cnotes, DiatonicPitch.parse('C:5'))
        
        vvoice_map = voice_note_map.get(violin_instrument_voice)
        vvoices = vvoice_map.keys()
        assert vvoice_map
        assert vvoices[0] in vvoice_map
        vnotes = vvoice_map[vvoices[0]]
        assert len(vnotes) == 3
        assert TestScore.has_pitch(vnotes, DiatonicPitch.parse('D:4'))
        assert TestScore.has_pitch(vnotes, DiatonicPitch.parse('E:4'))
        assert TestScore.has_pitch(vnotes, DiatonicPitch.parse('F:4'))
        
        duration = score.duration
        print 'full wnt duration = {0}'.format(duration)
        assert duration == Duration(1, 1)
        
        with self.assertRaises(Exception) as context:
            score.beat_duration
        self.assertTrue('sequences must be non-empty' in context.exception.message)
        
        # 3/4 TS + 60 beats per minute, 1 beat == 1 sec
        score.tempo_sequence.add(TempoEvent(Tempo(60), Position(0)))
        score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        bp_duration = score.beat_duration
        print 'full beat duration = {0}'.format(bp_duration)   
        
        assert bp_duration == BeatPosition(1, 1)   
        
        real_duration = score.real_duration 
        print 'real duration = {0}'.format(real_duration)  
        assert real_duration == 4000
        
    @staticmethod
    def has_class(classes, class_name):
        for n in classes:
            if n.name.lower() == class_name.lower():
                return True
        return False
    
    @staticmethod
    def has_pitch(notes, pitch):
        for n in notes:
            if n.diatonic_pitch == pitch:
                return True
        return False


if __name__ == "__main__":
    unittest.main()
