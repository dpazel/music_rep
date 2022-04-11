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
from midi.score_to_vst_midi_converter import ScoreToVstMidiConverter, NoteMessage

from timemodel.time_signature_event import TimeSignatureEvent
from structure.time_signature import TimeSignature
from timemodel.tempo_event import TempoEvent
from structure.tempo import Tempo
from timemodel.dynamics_event import DynamicsEvent
from structure.dynamics import Dynamics

from structure.beam import Beam


import logging


class TestScoreToVstMidiConverter(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_score_convert(self):
        print('test_score_convert')

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
        violin_voice_1.pin(vline_1, Offset(1, 16))

        # The test merges these two voices into one.

        svmc = ScoreToVstMidiConverter(score)
        meta_track, tracks = svmc.create({0: 4})
        assert meta_track is not None
        assert tracks is not None

        assert len(tracks) == 1
        assert len(tracks[0]) == 16

        for i in range(0, len(tracks[0])):
            print("{0}: {1}".format(i, tracks[0][i]))

        assert isinstance(tracks[0][0], NoteMessage)
        assert tracks[0][0].msg_type == 144
        assert tracks[0][0].note_value == 69   # A
        assert tracks[0][0].abs_frame_time == 0
        assert tracks[0][0].rel_frame_time == 0

        assert isinstance(tracks[0][3], NoteMessage)
        assert tracks[0][3].msg_type == 144
        assert tracks[0][3].note_value == 62   # D
        assert tracks[0][3].abs_frame_time == 10525
        assert tracks[0][3].rel_frame_time == 10525

        assert isinstance(tracks[0][5], NoteMessage)
        assert tracks[0][5].msg_type == 144
        assert tracks[0][5].note_value == 71   # B
        assert tracks[0][5].abs_frame_time == 21050
        assert tracks[0][5].rel_frame_time == 0

        assert isinstance(tracks[0][4], NoteMessage)
        assert tracks[0][4].msg_type == 128
        assert tracks[0][4].note_value == 69   # A
        assert tracks[0][4].abs_frame_time == 21050
        assert tracks[0][4].rel_frame_time == 10525

        assert isinstance(tracks[0][6], NoteMessage)
        assert tracks[0][6].msg_type == 128
        assert tracks[0][6].note_value == 62   # D
        assert tracks[0][6].abs_frame_time == 31575
        assert tracks[0][6].rel_frame_time == 10525

        assert isinstance(tracks[0][8], NoteMessage)
        assert tracks[0][8].msg_type == 128
        assert tracks[0][8].note_value == 71   # B
        assert tracks[0][8].abs_frame_time == 42100
        assert tracks[0][8].rel_frame_time == 10525

    def test_line_convert(self):
        print("test line convert")

        note1 = Note(DiatonicPitch(4, 'c'), Duration(1, 16))
        note2 = Note(DiatonicPitch(4, 'd'), Duration(1, 16))
        note3 = Note(DiatonicPitch(4, 'e'), Duration(1, 16))
        note4 = Note(DiatonicPitch(4, 'f'), Duration(1, 16))
        beam = Beam([note1, note2, note3, note4])

        line = Line(beam)

        meta_track, tracks = ScoreToVstMidiConverter.convert_line(line)
        assert meta_track is not None
        assert tracks is not None

        assert len(tracks) == 1
        assert len(tracks[0]) == 8

        for i in range(0, len(tracks[0])):
            print("{0}: {1}".format(i, tracks[0][i]))

        assert isinstance(tracks[0][0], NoteMessage)
        assert tracks[0][0].msg_type == 144
        assert tracks[0][0].note_value == 60   # C
        assert tracks[0][0].abs_frame_time == 0
        assert tracks[0][0].rel_frame_time == 0

        assert isinstance(tracks[0][2], NoteMessage)
        assert tracks[0][2].msg_type == 144
        assert tracks[0][2].note_value == 62   # D
        assert tracks[0][2].abs_frame_time == 10525
        assert tracks[0][2].rel_frame_time == 0

        assert isinstance(tracks[0][4], NoteMessage)
        assert tracks[0][4].msg_type == 144
        assert tracks[0][4].note_value == 64   # E
        assert tracks[0][4].abs_frame_time == 21050
        assert tracks[0][4].rel_frame_time == 0

        assert isinstance(tracks[0][6], NoteMessage)
        assert tracks[0][6].msg_type == 144
        assert tracks[0][6].note_value == 65   # F
        assert tracks[0][6].abs_frame_time == 31575
        assert tracks[0][6].rel_frame_time == 0
