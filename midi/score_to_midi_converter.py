"""

File: score_to_midi_converter.py

Purpose: Provides a means to convert a score to a midi file. 

"""
from mido import MidiFile, MidiTrack, Message

from fractions import Fraction

from timemodel.tempo_event import TempoEvent
from timemodel.time_signature_event import TimeSignatureEvent
from mido.midifiles import MetaMessage

from structure.dynamics import Dynamics
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from structure.score import Score

from timemodel.duration import Duration
from timemodel.position import Position
from timemodel.offset import Offset

from instruments.instrument_catalog import InstrumentCatalog
from structure.instrument_voice import InstrumentVoice

import logging
from timemodel.dynamics_event import DynamicsEvent
from timemodel.dynamics_function_event import DynamicsFunctionEvent
from misc.utility import convert_to_numeric
from timemodel.time_conversion import TimeConversion
from timemodel.tempo_function_event import TempoFunctionEvent
from timemodel.tempo_event_sequence import TempoEventSequence


class ScoreToMidiConverter(object):
    """
    This class is used to convert a score to a midi file.  The procedure is:
    1) Create a converter:  smc = ScoreToMidiConverter(score)
    2) Create the output file:  smc.create(filename)
    
    Note:
      All tempos messages are on channel 1 track 0
      All note messages are on channel 1 for other tracks.
    """
    
    # Number of MIDI ticks per quarter note.
    TICKS_PER_BEAT = 480
    DEFAULT_NOTE_CHANNEL = 1
    DEFAULT_VELOCITY = 64
    # number of ms between volume events for dynamic function events
    VOLUME_EVENT_DURATION_MS = 5
    TEMPO_EVENT_DURATION_MS = 50
    
    DEFAUTLT_BEAT_DURATION = Duration(1, 4)

    def __init__(self, score):
        """
        Constructor.  Set up the tick track map.
        
        Args:
          score:  of Score class 
        """
        
        self.__score = score
        self.__filename = ''
        self.__trace = False
        self.mid = None
        self.inst_voice_channel = {}
        self.channel_assignment = 1
        self.fine_tempo_sequence = None
        self.time_conversion = None
        
    def create(self, filename, trace=False):
        """
        Create a midi file from the score, with midi filename provided.
        
        Args:
          filename - String filename.  Can include path, should have filetype '.mid'.
        """
        self.__filename = filename
        self.__trace = trace
        
        self.mid = MidiFile(type=1)
        
        self.mid.ticks_per_beat = ScoreToMidiConverter.TICKS_PER_BEAT
        
        # assign each instrument voice to a channel
        self.inst_voice_channel = {}
        
        # used for assigning channels to each voice.
        self.channel_assignment = 1
                       
        (self.fine_tempo_sequence, self.time_conversion) = self._build_time_conversion()
                   
        meta_track = MidiTrack()
        self.mid.tracks.append(meta_track)
        self._fill_meta_track(meta_track)
        
        self._assign_voices_tracks()
        
        self.mid.save(self.filename)
        
    @property
    def score(self):
        return self.__score
    
    @property
    def filename(self):
        return self.__filename
    
    @staticmethod
    def convert_score(score, filename):
        """
        Static method to convert a Score to a midi file.
        
        Args:
          score: Class Score object
          filename: The name of the midi file, should have filetype .mid
        """
        smc = ScoreToMidiConverter(score)
        smc.create(filename)
        
    @staticmethod 
    def convert_line(line, filename, tempo=Tempo(60, Duration(1, 4)),
                     time_signature=TimeSignature(4, Duration(1, 4)), instrument_name='piano'):
        """
        Static method to convert a Line to a midi file
        
        Args:
          line: Class Line object
          filename: The name of the midi file, should have filetype .mid
          tempo: Tempo for playback, default is 60 BPM tempo beat = quarter note
          time_signature: TimeSiganture on playback, default is 4 quarter notes
          instrument_name: Name of instrument ot use for playback.
        """
        score = Score()
        tempo_sequence = score.tempo_sequence
        tempo_sequence.add(TempoEvent(tempo, Position(0)))
                
        ts_sequence = score.time_signature_sequence
        ts_sequence.add(TimeSignatureEvent(time_signature, Position(0)))
        
        c = InstrumentCatalog.instance() 
        instrument = c.get_instrument(instrument_name)
        if instrument is None:
            print('Error: instrument {0} cannnot be found'.format(instrument_name))
            return

        instrument_voice = InstrumentVoice(instrument, 1)
        piano_voice = instrument_voice.voice(0)
        
        piano_voice.pin(line, Offset(0))
              
        score.add_instrument_voice(instrument_voice)
        ScoreToMidiConverter.convert_score(score, filename)
    
    def _assign_voices_tracks(self):
        # assign a channel to each instrument voice
        for inst_voice in self.score.instrument_voices:
            self.inst_voice_channel[inst_voice] = self._next_channel()
            self._add_notes(inst_voice, self.inst_voice_channel[inst_voice])
            
    def _next_channel(self):
        """
        Allocates channels starting at 1 through 15. Raises exception beyond that.
        """
        if self.channel_assignment == 15:
            raise Exception('Ran out of channels.')
        self.channel_assignment += 1
        if self.channel_assignment == 9:  # drums
            return self._next_channel()
        return self.channel_assignment
            
    def _add_notes(self, inst_voice, channel):
        voice_note_map = inst_voice.get_all_notes()
        
        for voice, notes in voice_note_map.items():
            track = MidiTrack()
            track.name = inst_voice.instrument.name
            self.mid.tracks.append(track)
            # For each note
            #    build a note on and off message, compute the ticks of the message
            #    append both messages to out list msgs
            velocity_msgs = self._gen_velocity_msgs(voice, channel)
            msgs = [] 
            for n in notes:
                # We do not need to set velocity outside of the default 
                # Crescendo and decrescendo are taken care of by channel change messages only,
                #       which modify the constant velocity set per note.
                # If the velocity was set here, the channel  change would distort the setting.
                # Otherwise, the velocity would be acquired as follows
                ticks = self._wnt_to_ticks(n.get_absolute_position())
                msg = NoteMessage('note_on', channel, n.diatonic_pitch.chromatic_distance + 12, ticks,
                                  ScoreToMidiConverter.DEFAULT_VELOCITY)
                msgs.append(msg)
                end_ticks = self._wnt_to_ticks(n.get_absolute_position() + n.duration)
                msg = NoteMessage('note_off', channel, n.diatonic_pitch.chromatic_distance + 12, end_ticks)
                msgs.append(msg)
        
            # Sort the msgs list by tick time, and respect to off before on if same time
            msgs.extend(velocity_msgs)

            from functools import cmp_to_key
            msgs = sorted(msgs, key=cmp_to_key(lambda x, y: ScoreToMidiConverter.compare_note_msgs(x, y)))
    
            prior_tick = 0
            for m in msgs:
                logging.info('{0}'.format(m))
                ticks_value = int(m.abs_tick_time - prior_tick)
                # Append the midi message to the track, with tics being incremental over succeeding messages.
                # We default to channel 1 for all tracks.
                track.append(m.to_midi_message(ticks_value))
                prior_tick = m.abs_tick_time
                if self.__trace:
                    print('{0}/{1}'.format(ticks_value, m))
            
    def _gen_velocity_msgs(self, voice, channel):
        """
        The method runs through the dynamic sequence events, and generates channel change events to set velocity.
        In the case of a DynamicsEvent, the process is trivial.
        In the case of a DynamicsFunctionEvent, we generate channel change events in small steps over the domain
        of the event, providing a 'simulation' of velocity changes as dictated by the function behind the event.
        """
        msgs = []
        dyn_seq = voice.dynamics_sequence.sequence_list
        voice_len = voice.length()
        
        tc = self.time_conversion 
        
        for event in dyn_seq:
            if event.time >= voice_len:
                break
            if isinstance(event, DynamicsEvent):
                velocity = event.velocity()
                ticks = self._wnt_to_ticks(event.time)
                msgs.append(ExpressionVelocityMessage(channel, ticks, velocity))
            elif isinstance(event, DynamicsFunctionEvent):
                t1 = tc.position_to_actual_time(event.time)
                next_event = voice.dynamics_sequence.successor(event)
                t2 = tc.position_to_actual_time(next_event if next_event is not None else Position(voice_len.duration))
                while t1 < t2:
                    wnt = tc.actual_time_to_position(t1)
                    ticks = self._wnt_to_ticks(wnt)
                    velocity = int(event.velocity(wnt, next_event.time if next_event is not None else
                                   Position(voice_len.duration)))
                    msgs.append(ExpressionVelocityMessage(channel, ticks, velocity))
                    t1 += ScoreToMidiConverter.VOLUME_EVENT_DURATION_MS
                   
        return msgs
            
    def _fill_meta_track(self, meta_track):            
        event_list = self.score.tempo_sequence.sequence_list
        score_len = self.score.length()
        
        #  Loop over list, for every change in tempo , the tempo should be reset.
        #  Note, that there may be tempo or ts changes that last for 0 duration - we skip those.
        last_tick_time = 0
        for tempo_event in event_list:
            if tempo_event.time >= score_len:
                break
            if isinstance(tempo_event, TempoEvent):
                current_tick_time = self._wnt_to_ticks(tempo_event.time)
            
                # If there is a ts and tempo event, effect a midi tempo change
                beat_ratio = Fraction(1, 4) / tempo_event.object.beat_duration.duration
                
                # tempo_value = (60/BPM) * (ts_beat / tempo_beat)
                tempo_value = int((60.0 / tempo_event.object.tempo) * beat_ratio * 1000000)
                
                ticks = int(current_tick_time - last_tick_time)
                msg = MetaMessage('set_tempo', tempo=tempo_value, time=ticks)
                meta_track.append(msg)   
                last_tick_time = current_tick_time
            elif isinstance(tempo_event, TempoFunctionEvent):
                #  Run over event range making a small step function effectively, and setting the tempo
                #  every TEMPO_EVENT_DURATION_MS.
                t1 = tempo_event.time
                beat_duration = tempo_event.beat_duration if tempo_event.beat_duration is None else \
                    ScoreToMidiConverter.DEFAUTLT_BEAT_DURATION
                next_event = self.score.tempo_sequence.successor(tempo_event)
                t2 = next_event.time if next_event is not None else Position(score_len.duration)
                while t1 < t2:
                    tempo = int(tempo_event.tempo(t1, next_event.time if next_event is not None else
                                Position(score_len)))
                    delta_wnt = (tempo * ScoreToMidiConverter.TEMPO_EVENT_DURATION_MS * beat_duration.duration) / \
                                (60.0 * 1000.0)
                    
                    current_tick_time = self._wnt_to_ticks(t1)
                    ticks = int(current_tick_time - last_tick_time)
                    
                    # If there is a ts and tempo event, effect a midi tempo change
                    beat_ratio = Fraction(1, 4) / beat_duration.duration
                
                    # tempo_value = (60/BMP) * (ts_beat / tempo_beat)
                    tempo_value = int((60.0 / tempo) * beat_ratio * 1000000)
                    msg = MetaMessage('set_tempo', tempo=tempo_value, time=ticks)
                    meta_track.append(msg)                      
                    
                    t1 += delta_wnt
                    last_tick_time = current_tick_time
     
    def _build_time_conversion(self):
        event_list = self.score.tempo_sequence.sequence_list
        score_len = self.score.length()
        
        fine_tempo_sequence = TempoEventSequence()
        
        for event in event_list:
            if isinstance(event, TempoEvent):
                fine_tempo_sequence.add(TempoEvent(event.object, event.time))
            elif isinstance(event, TempoFunctionEvent):
                t1 = event.time
                beat_duration = event.beat_duration if event.beat_duration is None else \
                    ScoreToMidiConverter.DEFAUTLT_BEAT_DURATION
                next_event = self.score.tempo_sequence.successor(event)
                t2 = next_event.time if next_event is not None else Position(score_len.duration)
                while t1 < t2:
                    tempo = int(event.tempo(t1, next_event.time if next_event is not None else Position(score_len)))
                    delta_wnt = (tempo * ScoreToMidiConverter.TEMPO_EVENT_DURATION_MS * beat_duration.duration) / \
                                (60.0 * 1000.0)
                    
                    fine_tempo_sequence.add(TempoEvent(Tempo(tempo, beat_duration), t1))  

                    t1 += delta_wnt

        tc = TimeConversion(fine_tempo_sequence, self.score.time_signature_sequence, Position(score_len))  
        
        return fine_tempo_sequence, tc
                
    def _wnt_to_ticks(self, wnt):
        # Convert whole note time to ticks.
        offset = convert_to_numeric(wnt)
        return int((offset / Fraction(1, 4)) * self.mid.ticks_per_beat)
    
    @staticmethod
    def compare_note_msgs(a, b):
        a_ticks = a.abs_tick_time
        b_ticks = b.abs_tick_time
        comp_value = -1 if a_ticks < b_ticks else 1 if a_ticks > b_ticks else 0
        if isinstance(a, ExpressionVelocityMessage) or isinstance(b, ExpressionVelocityMessage):
            return comp_value
        
        if comp_value != 0:
            return comp_value
        a_is_note_off = a.msg_type == 'note_off'
        b_is_note_off = b.msg_type == 'note_off'
        if a_is_note_off and not b_is_note_off:
            return -1
        if not a_is_note_off and b_is_note_off:
            return 1
        return 0
       

class MidiMessage(object):
    
    def __init__(self, msg_type, channel, abs_tick_time):
        self.__msg_type = msg_type
        self.__channel = channel
        self.__abs_tick_time = abs_tick_time
        
    @property
    def msg_type(self):
        return self.__msg_type
    
    @property
    def channel(self):
        return self.__channel
    
    @property
    def abs_tick_time(self):
        return self.__abs_tick_time 
    
    def to_midi_message(self, prior_msg_ticks):
        return None   


class NoteMessage(MidiMessage):
    
    def __init__(self, msg_type, channel, note_value, abs_tick_time, velocity=Dynamics.DEFAULT_DYNAMICS_VELOCITY()):
        MidiMessage.__init__(self, msg_type, channel, abs_tick_time)
        self.__note_value = note_value
        self.__velocity = velocity
        
    @property
    def note_value(self):
        return self.__note_value
  
    @property
    def velocity(self):
        return self.__velocity
    
    def to_midi_message(self, ticks_from_prior_msg):
        return Message(self.msg_type, note=self.note_value, velocity=self.velocity, time=ticks_from_prior_msg,
                       channel=self.channel)
    
    def __str__(self):
        return '{0} {1}[{2}]:pv=({3}, {4})'.format(self.abs_tick_time, self.msg_type, self.channel, self.note_value,
                                                   self.velocity)


class ExpressionVelocityMessage(MidiMessage):
    
    def __init__(self, channel, abs_tick_time, velocity=Dynamics.DEFAULT_DYNAMICS_VELOCITY()):
        MidiMessage.__init__(self, 'control_change', channel, abs_tick_time)
        self.__velocity = velocity
    
    @property
    def velocity(self):
        return self.__velocity
    
    def to_midi_message(self, ticks_from_prior_msg):
        return Message(self.msg_type, control=11, value=self.velocity, time=ticks_from_prior_msg,
                       channel=self.channel)
    
    def __str__(self):
        return '{0} {1}/{2}({3})'.format(self.abs_tick_time, self.msg_type, self.channel, self.velocity)
