"""

File: score_to_vst_midi_converter.py

Purpose: Provides a means to convert a score to an object representation for vst.

"""
import logging
from fractions import Fraction

from structure.score import Score
from timemodel.tempo_event import TempoEvent
from timemodel.time_signature_event import TimeSignatureEvent

from timemodel.duration import Duration
from timemodel.position import Position
from timemodel.offset import Offset

from structure.dynamics import Dynamics
from structure.tempo import Tempo
from structure.time_signature import TimeSignature

from instruments.instrument_catalog import InstrumentCatalog
from structure.instrument_voice import InstrumentVoice

from timemodel.time_conversion import TimeConversion
from timemodel.tempo_function_event import TempoFunctionEvent
from timemodel.tempo_event_sequence import TempoEventSequence

from timemodel.dynamics_event import DynamicsEvent
from timemodel.dynamics_function_event import DynamicsFunctionEvent


class ScoreToVstMidiConverter(object):
    """
    This class is used to convert a score to a vst events.  The procedure is:
    1) Create a converter:  svmc = ScoreToVstMidiConverter(score)
    2) Create the output data:  meta_event, tracks = svmc.create()

    Note:
      All tempos messages are on channel 1 track 0
      All note messages are on channel 1 for other tracks.
    """

    # Number of MIDI ticks per quarter note

    DEFAULT_FRAME_RATE = 42100
    DEFAULT_VELOCITY = 64

    # number of ms between volume events for dynamic function events
    VOLUME_EVENT_DURATION_MS = 5
    TEMPO_EVENT_DURATION_MS = 50

    DEFAULT_BEAT_DURATION = Duration(1, 4)

    def __init__(self, score):
        """
        Constructor.  Set up the tick track map.

        Args:
          score:  of Score class
        """

        self.__score = score
        self.__filename = ''
        self.mid = None
        self.inst_voice_channel = {}
        self.fps = ScoreToVstMidiConverter.DEFAULT_FRAME_RATE
        self.channel_assignments = None
        self.fine_tempo_sequence = None
        self.time_conversion = None
        self.tracks = None
        self.channel_assignment = 0

        (self.fine_tempo_sequence, self.time_conversion) = self._build_time_conversion()

    def create(self, channel_assignments=None, fps=42100):
        """
        Create midi information from the score.

        Args:
          fps: frames per second setting
          channel_assignments: maps 0, 1,,, as track id to channel assignment.

        Returns:
            meta_track: list of tempo and time sig events
            tracks: list of tracks, each a list of vst midi events, ref. MidiMessage below.
        """
        self.fps = fps
        self.channel_assignments = channel_assignments
        self.tracks = list()

        # assign each instrument voice to a channel
        self.inst_voice_channel = {}
        self.used_channels = set()
        self.channel_assignment = 0

        meta_track = list()
        self._fill_meta_track(meta_track)

        self._assign_voices_tracks()

        return meta_track, self.tracks

    @staticmethod
    def convert_score(score, channel_assignments=None, fps=42100):
        """
        Static method to convert a Score to a midi file.

        Args:
          score: Class Score object
          filename: The name of the midi file, should have filetype .mid
        Returns:
            meta_track: list of tempo and time sig events
            tracks: list of tracks, each a list of vst midi events, ref. MidiMessage below.
        """
        smc = ScoreToVstMidiConverter(score)
        return smc.create(channel_assignments, fps)

    @staticmethod
    def convert_line(line, tempo=Tempo(60, Duration(1, 4)),
                     time_signature=TimeSignature(4, Duration(1, 4)), channel_assignments=None, fps=42100):
        """
        Static method to convert a Line to a midi file

        Args:
          line: Class Line object
          filename: The name of the midi file, should have filetype .mid
          tempo: Tempo for playback, default is 60 BPM tempo beat = quarter note
          time_signature: TimeSiganture on playback, default is 4 quarter notes
        """
        score = Score()
        tempo_sequence = score.tempo_sequence
        tempo_sequence.add(TempoEvent(tempo, Position(0)))

        ts_sequence = score.time_signature_sequence
        ts_sequence.add(TimeSignatureEvent(time_signature, Position(0)))

        c = InstrumentCatalog.instance()
        piano = c.get_instrument("piano")

        piano_instrument_voice = InstrumentVoice(piano, 1)
        piano_voice = piano_instrument_voice.voice(0)

        piano_voice.pin(line, Offset(0))

        score.add_instrument_voice(piano_instrument_voice)
        return ScoreToVstMidiConverter.convert_score(score, channel_assignments, fps)

    @property
    def score(self):
        return self.__score

    def _assign_voices_tracks(self):
        if self.channel_assignments:
            for inst_voice in self.score.instrument_voices:
                index = self.score.instrument_voices.index(inst_voice)
                if self.channel_assignments and index in self.channel_assignments:
                    self.inst_voice_channel[inst_voice] = self.channel_assignments[index]
                    self.used_channels.add(self.channel_assignments[index])

        # assign a channel to each instrument voice
        for inst_voice in self.score.instrument_voices:
            if inst_voice not in self.inst_voice_channel:
                self.inst_voice_channel[inst_voice] = self._next_channel()
            self._add_notes(inst_voice, self.inst_voice_channel[inst_voice])

    def _next_channel(self):
        """
        Allocates channels starting at 1 through 15. Raises exception beyond that.
        """
        if self.channel_assignment == 15:
            raise Exception('Ran out of channels.')
        self.channel_assignment += 1
        if self.channel_assignment in self.used_channels:
            return self._next_channel()
        if self.channel_assignment == 9:  # drums
            return self._next_channel()
        return self.channel_assignment

    def _add_notes(self, inst_voice, channel):
        voice_note_map = inst_voice.get_all_notes()

        track = list()

        for voice, notes in voice_note_map.items():
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
                frames = self._wnt_to_fps(n.get_absolute_position())
                msg = NoteMessage(NoteMessage.NOTE_ON, channel, n.diatonic_pitch.chromatic_distance + 12, frames,
                                  ScoreToVstMidiConverter.DEFAULT_VELOCITY)
                msgs.append(msg)
                end_frames = self._wnt_to_fps(n.get_absolute_position() + n.duration)
                msg = NoteMessage(NoteMessage.NOTE_OFF, channel, n.diatonic_pitch.chromatic_distance + 12, end_frames)
                msgs.append(msg)

            # Sort the msgs list by tick time, and respect to off before on if same time
            msgs.extend(velocity_msgs)
            track.extend(msgs)

        from functools import cmp_to_key
        track = sorted(track, key=cmp_to_key(lambda x, y: ScoreToVstMidiConverter.compare_note_msgs(x, y)))

        self.tracks.append(track)

        prior_frame = 0
        for m in track:
            logging.info('{0}'.format(m))
            frames_value = int(m.abs_frame_time - prior_frame)
            # Append the midi message to the track, with tics being incremental over succeeding messages.
            # We default to channel 1 for all tracks.
            prior_frame = m.abs_frame_time
            m.set_rel_frame_time(frames_value)

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
                frames = self._wnt_to_fps(event.time)
                msgs.append(ExpressionVelocityMessage(channel, frames, velocity))
            elif isinstance(event, DynamicsFunctionEvent):
                t1 = tc.position_to_actual_time(event.time)
                next_event = voice.dynamics_sequence.successor(event)
                t2 = tc.position_to_actual_time(next_event if next_event is not None else Position(voice_len.duration))
                while t1 < t2:
                    wnt = tc.actual_time_to_position(t1)
                    frames = self._wnt_to_fps(wnt)
                    velocity = int(event.velocity(wnt, next_event.time if next_event is not None else
                                                       Position(voice_len.duration)))
                    msgs.append(ExpressionVelocityMessage(channel, frames, velocity))
                    t1 += ScoreToVstMidiConverter.VOLUME_EVENT_DURATION_MS

        return msgs

    def _fill_meta_track(self, meta_track):
        event_list = self.score.tempo_sequence.sequence_list
        score_len = self.score.length()

        #  Loop over list, for every change in tempo , the tempo should be reset.
        #  Note, that there may be tempo or ts changes that last for 0 duration - we skip those.
        last_fps_time = 0
        for tempo_event in event_list:
            if tempo_event.time >= score_len:
                break
            if isinstance(tempo_event, TempoEvent):
                current_fps_time = self._wnt_to_fps(tempo_event.time)

                # If there is a ts and tempo event, effect a midi tempo change
                beat_ratio = Fraction(1, 4) / tempo_event.object.beat_duration.duration

                # tempo_value = (60/BPM) * (ts_beat / tempo_beat)
                tempo_value = int((60.0 / tempo_event.object.tempo) * beat_ratio * 1000000)

                frames = int(current_fps_time - last_fps_time)
                msg = MetaMessage(MetaMessage.TEMPO_MESSAGE, tempo_value, frames)
                meta_track.append(msg)
                last_fps_time = current_fps_time
            elif isinstance(tempo_event, TempoFunctionEvent):
                #  Run over event range making a small step function effectively, and setting the tempo
                #  every TEMPO_EVENT_DURATION_MS.
                t1 = tempo_event.time
                beat_duration = tempo_event.beat_duration if tempo_event.beat_duration is None else \
                    ScoreToVstMidiConverter.DEFAULT_BEAT_DURATION
                next_event = self.score.tempo_sequence.successor(tempo_event)
                t2 = next_event.time if next_event is not None else Position(score_len.duration)
                while t1 < t2:
                    tempo = int(tempo_event.tempo(t1, next_event.time if next_event is not None
                                                                      else Position(score_len)))
                    delta_wnt = (tempo * ScoreToVstMidiConverter.TEMPO_EVENT_DURATION_MS * beat_duration.duration) / \
                                (60.0 * 1000.0)

                    current_fps_time = self._wnt_to_fps(t1)
                    frames = int(current_fps_time - last_fps_time)

                    # If there is a ts and tempo event, effect a midi tempo change
                    beat_ratio = Fraction(1, 4) / beat_duration.duration

                    # tempo_value = (60/BMP) * (ts_beat / tempo_beat)
                    tempo_value = int((60.0 / tempo) * beat_ratio * 1000000)
                    msg = MetaMessage(MetaMessage.TEMPO_MESSAGE, tempo_value, frames)
                    meta_track.append(msg)

                    t1 += delta_wnt
                    last_fps_time = current_fps_time

    def _wnt_to_fps(self, wnt):
        # Convert whole note time to fps.
        return int((self.time_conversion.position_to_actual_time(wnt) * self.fps)/ 1000.0)

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
                    ScoreToVstMidiConverter.DEFAULT_BEAT_DURATION
                next_event = self.score.tempo_sequence.successor(event)
                t2 = next_event.time if next_event is not None else Position(score_len.duration)
                while t1 < t2:
                    tempo = int(event.tempo(t1, next_event.time if next_event is not None else Position(score_len)))
                    delta_wnt = (tempo * ScoreToVstMidiConverter.TEMPO_EVENT_DURATION_MS * beat_duration.duration) / \
                                (60.0 * 1000.0)

                    fine_tempo_sequence.add(TempoEvent(Tempo(tempo, beat_duration), t1))

                    t1 += delta_wnt

        tc = TimeConversion(fine_tempo_sequence, self.score.time_signature_sequence, Position(score_len))

        return fine_tempo_sequence, tc

    @staticmethod
    def compare_note_msgs(a, b):
        a_frames = a.abs_frame_time
        b_frames = b.abs_frame_time
        comp_value = -1 if a_frames < b_frames else 1 if a_frames > b_frames else 0
        if isinstance(a, ExpressionVelocityMessage) or isinstance(b, ExpressionVelocityMessage):
            return comp_value

        if comp_value != 0:
            return comp_value
        a_is_note_off = a.msg_type == NoteMessage.NOTE_OFF
        b_is_note_off = b.msg_type == NoteMessage.NOTE_OFF
        if a_is_note_off and not b_is_note_off:
            return -1
        if not a_is_note_off and b_is_note_off:
            return 1
        return 0


class MidiMessage(object):

    def __init__(self, msg_type, channel, abs_frame_time):
        self.__msg_type = msg_type
        self.__channel = channel
        self.__abs_frame_time = abs_frame_time
        self.__rel_frame_time = 0

    @property
    def msg_type(self):
        return self.__msg_type

    @property
    def channel(self):
        return self.__channel

    @property
    def abs_frame_time(self):
        return self.__abs_frame_time

    @property
    def rel_frame_time(self):
        return self.__rel_frame_time

    def set_rel_frame_time(self, fps):
        self.__rel_frame_time = fps


class NoteMessage(MidiMessage):

    NOTE_ON = 0x90
    NOTE_OFF = 0x80

    def __init__(self, msg_type, channel, note_value, abs_frame_time, velocity=Dynamics.DEFAULT_DYNAMICS_VELOCITY):
        MidiMessage.__init__(self, msg_type, channel, abs_frame_time)
        self.__note_value = note_value
        self.__velocity = velocity

    @property
    def note_value(self):
        return self.__note_value

    @property
    def velocity(self):
        return self.__velocity

    def __str__(self):
        return '{0}/{1} {2}[{3}]({4}, {5})'.format(self.abs_frame_time, self.rel_frame_time, self.msg_type,
                                                  self.channel, self.note_value,
                                                  self.velocity)


class MetaMessage(MidiMessage):

    TEMPO_MESSAGE = -1
    TIME_SIGNATURE_EVENT = -2

    def __init__(self, message_type, value, abs_frame_time):
        MidiMessage.__init__(self, message_type, 0, abs_frame_time)
        self.__value = value

    @property
    def value(self):
        return self.__value


class ExpressionVelocityMessage(MidiMessage):

    def __init__(self, channel, abs_frame_time, velocity=Dynamics.DEFAULT_DYNAMICS_VELOCITY):
        MidiMessage.__init__(self, 0xB0, channel, abs_frame_time)
        self.__velocity = velocity

    @property
    def velocity(self):
        return self.__velocity

    def __str__(self):
        return '{0}/{1} {2}[{3}] ({4})'.format(self.abs_frame_time, self.rel_frame_time, self.msg_type, self.channel,
                                               self.velocity)
