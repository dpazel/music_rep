import unittest

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from instruments.instrument_catalog import InstrumentCatalog
from structure.lite_score import LiteScore
from structure.line import Line
from structure.note import Note
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.tempo_event_sequence import TempoEventSequence
from tonalmodel.diatonic_pitch import DiatonicPitch
from timemodel.position import Position

from timemodel.time_signature_event import TimeSignatureEvent
from structure.time_signature import TimeSignature, BeatType
from timemodel.tempo_event import TempoEvent
from structure.tempo import Tempo

from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality

from fractions import Fraction


class TestLiteScore(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_setup(self):
        c = InstrumentCatalog.instance()
        violin = c.get_instrument("violin")

        # Add notes to the score
        vnote0 = Note(DiatonicPitch(4, 'a'), Duration(1, 8))
        vnote1 = Note(DiatonicPitch(4, 'b'), Duration(1, 8))
        vnote2 = Note(DiatonicPitch(4, 'c'), Duration(1, 8))
        vnote3 = Note(DiatonicPitch(4, 'd'), Duration(1, 8))
        vnote4 = Note(DiatonicPitch(4, 'e'), Duration(1, 8))
        vnote5 = Note(DiatonicPitch(4, 'f'), Duration(1, 8))

        # Set up a violin voice with 6 8th notes
        vline = Line([vnote0, vnote1, vnote2, vnote3, vnote4, vnote5])

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4), 'sww'), Position(0)))

        hc_track = HarmonicContextTrack()
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(2)))

        score = LiteScore(vline, hc_track, violin, tempo_seq, ts_seq)

        bp = score.beat_position(Position(0))
        print(bp)
        assert bp.beat_number == 0

        bp = score.beat_position(Position(5, 8))
        print(bp)
        assert bp.measure_number == 0
        assert bp.beat_number == Fraction(5, 2)
        assert int(bp.beat_number) == 2
        assert bp.beat_number - bp.beat == Fraction(1, 2)

        tse = score.time_signature_sequence.floor_event(Position(5, 8))
        assert tse is not None
        print(tse.object.beat_type(bp.beat))
        assert tse.object.beat_type(bp.beat) == BeatType.Weak
        assert bp.beat_fraction == Fraction(1, 2)

        bp = score.beat_position(Position(1, 16))
        print(bp)
        tse = score.time_signature_sequence.floor_event(Position(1, 16))
        print(tse.object.beat_type(bp.beat))
        assert tse.object.beat_type(bp.beat) == BeatType.Strong
