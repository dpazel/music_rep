import unittest
from instruments.instrument_catalog import InstrumentCatalog
from structure.score import Score
from structure.instrument_voice import InstrumentVoice
from structure.line import Line
from structure.note import Note
from timemodel.duration import Duration
from timemodel.position import Position
from timemodel.offset import Offset
from tonalmodel.diatonic_pitch import DiatonicPitch
from midi.score_to_midi_converter import ScoreToMidiConverter

from timemodel.time_signature_event import TimeSignatureEvent
from structure.time_signature import TimeSignature
from timemodel.tempo_event import TempoEvent
from structure.tempo import Tempo
from timemodel.dynamics_event import DynamicsEvent
from structure.dynamics import Dynamics

from structure.beam import Beam

from mido import MidiFile

import logging
from timemodel.dynamics_function_event import DynamicsFunctionEvent
from function.piecewise_linear_function import PiecewiseLinearFunction
from timemodel.tempo_function_event import TempoFunctionEvent


class TestScoreToMidiConverter(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_score_convert(self):
        c = InstrumentCatalog.instance()   
        
        score = Score()
        
        score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        score.tempo_sequence.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
            
        violin = c.get_instrument("violin")
        violin_instrument_voice = InstrumentVoice(violin, 2)
        violin_voice_0 = violin_instrument_voice.voice(0)
        violin_voice_1 = violin_instrument_voice.voice(1)
        assert violin_voice_0
        assert violin_voice_1
        score.add_instrument_voice(violin_instrument_voice)
        
        violin_voice_0.dynamics_sequence.add(DynamicsEvent(Dynamics(Dynamics.P), Position(0)))
        violin_voice_0.dynamics_sequence.add(DynamicsEvent(Dynamics(Dynamics.FFF), Position(1, 4)))
        violin_voice_1.dynamics_sequence.add(DynamicsEvent(Dynamics(Dynamics.P), Position(0)))
        violin_voice_1.dynamics_sequence.add(DynamicsEvent(Dynamics(Dynamics.FFF), Position(1, 4)))
        
        # Add notes to the score
        vnote0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        vnote1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        vnote2 = Note(DiatonicPitch(5, 'c'), Duration(1, 8))     
        vnote3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8)) 
        vnote4 = Note(DiatonicPitch(4, 'e'), Duration(1, 8))     
        vnote5 = Note(DiatonicPitch(4, 'f'), Duration(1, 8))   
        
        # Set up a violin voice with 6 8th notes 
        vline_0 = Line([vnote0, vnote1, vnote2])
        violin_voice_0.pin(vline_0)
        
        # Set up a violin voice with 6 8th notes
        vline_1 = Line([vnote3, vnote4, vnote5])
        violin_voice_1.pin(vline_1)
        
        smc = ScoreToMidiConverter(score)
        smc.create('score_output_file.mid')

        TestScoreToMidiConverter.read_midi_file('score_output_file.mid')
        
    def test_line_convert(self):
        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 16))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 16))
        note3 = Note(DiatonicPitch(4, 'e'), Duration(1, 16))
        note4 = Note(DiatonicPitch(4, 'f'), Duration(1, 16))
        beam = Beam([note1, note2, note3, note4]) 
        
        line = Line(beam)
        
        ScoreToMidiConverter.convert_line(line, 'line_output_file.mid')

        TestScoreToMidiConverter.read_midi_file('line_output_file.mid')
        
    def test_multi_track(self):
        c = InstrumentCatalog.instance()   
        
        score = Score()
        
        score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        score.tempo_sequence.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
            
        violin = c.get_instrument("violin")
        piano = c.get_instrument("piano")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(1, 4))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 4))
        note2 = Note(DiatonicPitch(4, 'c'), Duration(1, 4))     
        note3 = Note(DiatonicPitch(4, 'd'), Duration(1, 4)) 
        note4 = Note(DiatonicPitch(5, 'g'), Duration(1, 4))     
        note5 = Note(DiatonicPitch(5, 'f'), Duration(1, 4)) 
        note6 = Note(DiatonicPitch(5, 'e'), Duration(1, 4)) 
        note7 = Note(DiatonicPitch(5, 'd'), Duration(1, 4))
     
        violin_instrument_voice = InstrumentVoice(violin, 1)
        violin_voice = violin_instrument_voice.voice(0)
        assert violin_voice
                       
        vline = Line([note0, note1, note2, note3])
        violin_voice.pin(vline)
        
        score.add_instrument_voice(violin_instrument_voice)
        
        piano_instrument_voice = InstrumentVoice(piano, 1)
        piano_voice = piano_instrument_voice.voice(0)
        assert piano_voice
        
        pline = Line([note4, note5, note6, note7])
        piano_voice.pin(pline, Offset(1, 8))

        score.add_instrument_voice(piano_instrument_voice)
        
        violin_voice.dynamics_sequence.add(DynamicsEvent(Dynamics(Dynamics.F), Position(0)))
        piano_voice.dynamics_sequence.add(DynamicsEvent(Dynamics(Dynamics.P), Position(0)))
        
        smc = ScoreToMidiConverter(score)
        smc.create('score_multi_trackoutput_file.mid')

        TestScoreToMidiConverter.read_midi_file('score_multi_trackoutput_file.mid')
        
    def test_dynamic_volume(self):
        c = InstrumentCatalog.instance()   
        
        score = Score()
        
        score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        score.tempo_sequence.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
            
        violin = c.get_instrument("violin")
        
        note0 = Note(DiatonicPitch(4, 'a'), Duration(3, 2))
        note1 = Note(DiatonicPitch(4, 'b'), Duration(1, 2))
        note2 = Note(DiatonicPitch(5, 'c'), Duration(1, 2))     
        note3 = Note(DiatonicPitch(5, 'd'), Duration(1, 4)) 
        note4 = Note(DiatonicPitch(5, 'g'), Duration(1, 4))     
        note5 = Note(DiatonicPitch(5, 'f'), Duration(1, 4)) 
        note6 = Note(DiatonicPitch(5, 'e'), Duration(1, 4)) 
        note7 = Note(DiatonicPitch(5, 'd'), Duration(1, 4))
     
        violin_instrument_voice = InstrumentVoice(violin, 1)
        violin_voice = violin_instrument_voice.voice(0)
        assert violin_voice
                       
        vline = Line([note0, note1, note2, note3, note4, note5, note6, note7])
        violin_voice.pin(vline)
        
        score.add_instrument_voice(violin_instrument_voice)
        
        # create a crescendo
        
        v_low = Dynamics.PPP.velocity
        v_hi = Dynamics.FFFF.velocity
        array = [(Position(0), v_low),
                 (Position(3, 2), v_hi)
                 ]
        f = PiecewiseLinearFunction(array)
        event1 = DynamicsFunctionEvent(f, Position(0))
             
        violin_voice.dynamics_sequence.add(event1)
        
        smc = ScoreToMidiConverter(score)
        smc.create('score_vary_volume_file.mid')

        TestScoreToMidiConverter.read_midi_file('score_vary_volume_file.mid')
        
    def test_tempo_change(self):
        c = InstrumentCatalog.instance()   
        
        score = Score()
        
        score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        score.tempo_sequence.add(TempoEvent(Tempo(120, Duration(1, 4)), Position(0)))
        score.tempo_sequence.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(1)))
        score.tempo_sequence.add(TempoEvent(Tempo(30, Duration(1, 4)), Position(2)))
            
        violin = c.get_instrument("violin")
        violin_instrument_voice = InstrumentVoice(violin, 1)
        violin_voice_0 = violin_instrument_voice.voice(0)
        assert violin_voice_0
        score.add_instrument_voice(violin_instrument_voice)
        
        violin_voice_0.dynamics_sequence.add(DynamicsEvent(Dynamics(Dynamics.F), Position(0)))

        # Add notes to the score
        vnote0 = Note(DiatonicPitch(4, 'a'), Duration(1, 4))
        vnote1 = Note(DiatonicPitch(4, 'b'), Duration(1, 4))
        vnote2 = Note(DiatonicPitch(5, 'c'), Duration(1, 4))     
        vnote3 = Note(DiatonicPitch(5, 'd'), Duration(1, 4)) 
        
        vnote4 = Note(DiatonicPitch(4, 'a'), Duration(1, 4))
        vnote5 = Note(DiatonicPitch(4, 'b'), Duration(1, 4))
        vnote6 = Note(DiatonicPitch(5, 'c'), Duration(1, 4))     
        vnote7 = Note(DiatonicPitch(5, 'd'), Duration(1, 4))
        
        vnote8 = Note(DiatonicPitch(4, 'a'), Duration(1, 4))
        vnote9 = Note(DiatonicPitch(4, 'b'), Duration(1, 4))
        vnote10 = Note(DiatonicPitch(5, 'c'), Duration(1, 4))     
        vnote11 = Note(DiatonicPitch(5, 'd'), Duration(1, 4))

        # Set up a violin voice with 6 8th notes 
        vline_0 = Line([vnote0, vnote1, vnote2, vnote3, vnote4, vnote5, vnote6, vnote7,
                        vnote8, vnote9, vnote10, vnote11])
        violin_voice_0.pin(vline_0)
        
        # Set up a violin voice with 6 8th notes
        vline_1 = Line([vnote0, vnote1, vnote2, vnote3])
        violin_voice_0.pin(vline_1)
        
        smc = ScoreToMidiConverter(score)
        smc.create('score_tempo_change_file.mid')

        TestScoreToMidiConverter.read_midi_file('score_tempo_change_file.mid')
        
    def test_variable_tempo_change(self):
        c = InstrumentCatalog.instance()   
        
        score = Score()
        
        violin = c.get_instrument("violin")
        violin_instrument_voice = InstrumentVoice(violin, 1)
        violin_voice = violin_instrument_voice.voice(0)
        assert violin_voice
        score.add_instrument_voice(violin_instrument_voice)
        
        score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        
        score.tempo_sequence.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))  
        
        t_low = 60
        t_hi = 250
        array = [(Position(0), t_low),
                 (Position(1), t_hi),
                 (Position(2), t_hi),
                 (Position(3), t_low)
                 ]
        f = PiecewiseLinearFunction(array)
        event1 = TempoFunctionEvent(f, Position(1)) 
        score.tempo_sequence.add(event1)
        
        score.tempo_sequence.add(TempoEvent(Tempo(t_low, Duration(1, 4)), Position(4))) 
        
        # create notes
        notes = []
        for _ in range(0, 6):
            notes.append(Note(DiatonicPitch(4, 'c'), Duration(1, 4)))
            notes.append(Note(DiatonicPitch(4, 'd'), Duration(1, 4)))
            notes.append(Note(DiatonicPitch(4, 'e'), Duration(1, 4)))     
            notes.append(Note(DiatonicPitch(4, 'f'), Duration(1, 4))) 
        vline = Line(notes)
        violin_voice.pin(vline) 
        
        smc = ScoreToMidiConverter(score)
        smc.create('score_var_tempo_change_file.mid')

        TestScoreToMidiConverter.read_midi_file('score_var_tempo_change_file.mid')
               
    @staticmethod
    def read_midi_file(filename):
        print('Opening {0}'.format(filename))
        mid = MidiFile(filename)
        ticks_per_beat = mid.ticks_per_beat
        print('ticks per beat {0}'.format(ticks_per_beat))
    
        for i, track in enumerate(mid.tracks):
            print('Track {}: {}'.format(i, track.name))
            for message in track:
                print(message)
    
        print('Exiting read_midi_file {0} length {1} seconds'.format(filename, mid.length))

    def test_score_book_example(self):
        score = Score()

        catalogue = InstrumentCatalog.instance()
        score.add_instrument_voice(InstrumentVoice(catalogue.get_instrument("violin")))

        score.tempo_sequence.add(TempoEvent(Tempo(60), Position(0)))
        score.time_signature_sequence.add(TimeSignatureEvent(TimeSignature(4, Duration(1, 4)), Position(0)))

        violin_voice = score.get_instrument_voice("violin")[0]
        note_1 = Note(DiatonicPitch(4, 'A'), Duration(1, 4))
        note_2 = Note(DiatonicPitch(5, 'C'), Duration(1, 8))
        note_3 = Note(DiatonicPitch(5, 'B'), Duration(1, 8))
        note_4 = Note(DiatonicPitch(5, 'D'), Duration(1, 4))
        note_5 = Note(DiatonicPitch(5, 'E'), Duration(1, 8))
        note_6 = Note(DiatonicPitch(5, 'D'), Duration(1, 8))
        note_7 = Note(DiatonicPitch(4, 'G'), Duration(1, 4))
        note_8 = Note(DiatonicPitch(4, 'C'), Duration(1, 4))
        line = Line([note_1, note_2, note_3, note_4, note_5, note_6, note_7, note_8])
        violin_voice.voice(0).pin(line)

        smc = ScoreToMidiConverter(score)
        smc.create('book_example_midi_file.mid', True)

        ScoreToMidiConverter.convert_line(line, 'line_example_midi_file.mid', Tempo(90, Duration(1, 8)),
                                          instrument_name='violin')
