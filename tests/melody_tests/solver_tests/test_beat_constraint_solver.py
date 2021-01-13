import unittest
import logging
import sys

from harmonicmodel.tertian_chord_template import TertianChordTemplate
from melody.solver.beat_constraint_solver import BeatConstraintSolver
from melody.constraints.on_beat_constraint import OnBeatConstraint
from structure.beam import Beam
from structure.line import Line
from structure.lite_score import LiteScore
from structure.note import Note
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from structure.tuplet import Tuplet
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.offset import Offset
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from tonalmodel.diatonic_pitch import DiatonicPitch
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmoniccontext.harmonic_context import HarmonicContext
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.diatonic_tone import DiatonicTone
from instruments.instrument_catalog import InstrumentCatalog
from structure.time_signature import BeatType


class TestBeatConstraintSolver(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_setup(self):
        print('--- test_simple_setup')
        line = Line()

        notes = [
            Note(DiatonicPitch.parse('a:4'), Duration(1, 4)),
            Note(DiatonicPitch.parse('b:4'), Duration(1, 4)),
            Note(DiatonicPitch.parse('c:4'), Duration(1, 4)),
            Note(DiatonicPitch.parse('d:4'), Duration(1, 4)),
            Note(DiatonicPitch.parse('e:4'), Duration(1, 2)),
            Note(DiatonicPitch.parse('f:4'), Duration(1, 2)),
        ]

        location = 0
        for note in notes:
            line.pin(note, Offset(location))
            location += note.duration.duration

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4), 'sww'), Position(0)))

        harmonic_context_track = HarmonicContextTrack()
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))

        c = InstrumentCatalog.instance()
        violin = c.get_instrument("violin")

        score = LiteScore(line, harmonic_context_track, violin, tempo_seq, ts_seq)

        # Test everything is ok
        on_beat_constraints = [
            OnBeatConstraint(notes[0],  BeatType.Strong)
        ]

        bce = BeatConstraintSolver.create(score, on_beat_constraints)

        results = bce.solve()
        assert results is not None
        assert len(results) == 0

        # Test making the first and third beat strong
        on_beat_constraints = [
            OnBeatConstraint(notes[0], BeatType.Strong),
            OnBeatConstraint(notes[2], BeatType.Strong)
        ]

        bce = BeatConstraintSolver.create(score, on_beat_constraints)

        results = bce.solve()
        assert results is not None
        assert len(results) == 1

        print(results[0])
        new_line = results[0].apply(True)
        print(new_line)

        all_notes = new_line.get_all_notes()
        assert Position(3, 4) == all_notes[2].get_absolute_position()
        assert Position(1) == all_notes[3].get_absolute_position()
        assert Position(5, 4) == all_notes[4].get_absolute_position()

        # Test making the first and third and fifth beat strong
        on_beat_constraints = [
            OnBeatConstraint(notes[0], BeatType.Strong),
            OnBeatConstraint(notes[2], BeatType.Strong),
            OnBeatConstraint(notes[4], BeatType.Strong)
        ]

        bce = BeatConstraintSolver(line, tempo_seq, ts_seq, HarmonicContextTrack(), on_beat_constraints)

        results = bce.solve()
        assert results is not None
        assert len(results) == 1

        print(results[0])
        new_line = results[0].apply(True)
        print(new_line)

        all_notes = new_line.get_all_notes()
        assert Position(3, 4) == all_notes[2].get_absolute_position()
        assert Position(1) == all_notes[3].get_absolute_position()
        assert Position(3, 2) == all_notes[4].get_absolute_position()
        assert Position(2, 1) == all_notes[5].get_absolute_position()

    def test_structural_move(self):
        beam_notes = [
            Note(DiatonicPitch.parse('a:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('b:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('c:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('d:3'), Duration(1, 8)),
        ]
        beam = Beam(beam_notes)

        tuplet_notes = [
            Note(DiatonicPitch.parse('a:5'), Duration(1, 8)),
            Note(DiatonicPitch.parse('b:5'), Duration(1, 8)),
            Note(DiatonicPitch.parse('c:5'), Duration(1, 8)),
        ]
        tuplet = Tuplet(Duration(1, 8), 2, tuplet_notes)

        line = Line()

        notes = [
            Note(DiatonicPitch.parse('a:4'), Duration(1, 4)),
            Note(DiatonicPitch.parse('b:4'), Duration(1, 4)),
            beam,
            Note(DiatonicPitch.parse('d:4'), Duration(1, 4)),
            tuplet,
            Note(DiatonicPitch.parse('f:4'), Duration(1, 2)),
        ]

        location = 0
        for note_str in notes:
            line.pin(note_str, Offset(location))
            location += note_str.duration.duration

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(4, Duration(1, 4), 'swww'), Position(0)))

        harmonic_context_track = HarmonicContextTrack()
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))

        c = InstrumentCatalog.instance()
        violin = c.get_instrument("violin")

        score = LiteScore(line, harmonic_context_track, violin, tempo_seq, ts_seq)

        # Test everything is ok
        on_beat_constraints = [
            OnBeatConstraint(notes[0],  BeatType.Strong),
            OnBeatConstraint(beam_notes[1], BeatType.Strong),
            OnBeatConstraint(tuplet_notes[0], BeatType.Strong),
        ]

        print(line)

        bce = BeatConstraintSolver.create(score, on_beat_constraints)

        results = bce.solve()
        assert results is not None
        assert len(results) == 1

        print(results[0])
        new_line = results[0].apply(True)
        print(new_line)

        line_notes = new_line.get_all_notes()
        assert Position(7, 8) == line_notes[2].get_absolute_position()
        assert Position(1) == line_notes[3].get_absolute_position()
        assert Position(2) == line_notes[7].get_absolute_position()

    def test_multiple_ts(self):
        print('--- test_muliple_ts')
        beam_notes = [
            Note(DiatonicPitch.parse('a:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('b:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('c:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('d:3'), Duration(1, 8)),
        ]
        beam = Beam(beam_notes)

        tuplet_notes = [
            Note(DiatonicPitch.parse('a:5'), Duration(1, 8)),
            Note(DiatonicPitch.parse('b:5'), Duration(1, 8)),
            Note(DiatonicPitch.parse('c:5'), Duration(1, 8)),
        ]
        tuplet = Tuplet(Duration(1, 8), 2, tuplet_notes)

        line = Line()

        notes = [
            Note(DiatonicPitch.parse('a:4'), Duration(1, 4)),
            Note(DiatonicPitch.parse('b:4'), Duration(1, 4)),
            beam,
            Note(DiatonicPitch.parse('d:4'), Duration(1, 4)),
            tuplet,
            Note(DiatonicPitch.parse('f:4'), Duration(1, 2)),
        ]

        location = 0
        for note_str in notes:
            line.pin(note_str, Offset(location))
            location += note_str.duration.duration

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(4, Duration(1, 4), 'swww'), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4), 'sww'), Position(1)))

        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))

        c = InstrumentCatalog.instance()
        violin = c.get_instrument("violin")

        score = LiteScore(line, hc_track, violin, tempo_seq, ts_seq)

        # Test everything is ok
        on_beat_constraints = [
            OnBeatConstraint(notes[0],  BeatType.Strong),
            OnBeatConstraint(beam_notes[1], BeatType.Strong),
            OnBeatConstraint(tuplet_notes[0], BeatType.Strong),
            OnBeatConstraint(notes[5], BeatType.Strong),
        ]

        print(line)

        bce = BeatConstraintSolver.create(score, on_beat_constraints)

        results = bce.solve()
        assert results is not None
        assert len(results) == 1

        print(results[0])
        new_line = results[0].apply(True)
        print(new_line)

        all_notes = new_line.get_all_notes()
        assert Position(1, 1) == all_notes[3].get_absolute_position()
        assert Position(17, 8) == all_notes[7].get_absolute_position()
        assert Position(23, 8) == all_notes[10].get_absolute_position()

        # Check the hct for this pdi
        hct = results[0].hct
        assert 3 == len(hct)
        hc_list = hct.hc_list()
        assert Duration(11, 8) == hc_list[0].duration
        assert Duration(2) == hc_list[1].duration
        assert Duration(1) == hc_list[2].duration

        assert Position(0) == hc_list[0].position
        assert Position(11, 8) == hc_list[1].position
        assert Position(27, 8) == hc_list[2].position
