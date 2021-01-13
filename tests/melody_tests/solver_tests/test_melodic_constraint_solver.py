import unittest
import logging
import sys

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from instruments.instrument_catalog import InstrumentCatalog
from melody.constraints.on_beat_constraint import OnBeatConstraint
from melody.constraints.step_sequence_constraint import StepSequenceConstraint
from melody.solver.melodic_constraint_solver import MelodicConstraintSolver
from structure.line import Line
from structure.lite_score import LiteScore
from structure.note import Note
from structure.tempo import Tempo
from structure.time_signature import TimeSignature, BeatType
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.offset import Offset
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality


class TestMelodicConstraintSolver(unittest.TestCase):
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

        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 1)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))

        c = InstrumentCatalog.instance()
        violin = c.get_instrument("violin")

        score = LiteScore(line, hc_track, violin, tempo_seq, ts_seq)

        constraints = [
            OnBeatConstraint(notes[1],  BeatType.Strong),
            StepSequenceConstraint(notes, [1, 1, 1, -1, -1])
        ]

        solver = MelodicConstraintSolver.create(score, constraints)

        cheat = {notes[2]: DiatonicPitch.parse('E:5')}

        results = solver.solve(cheat)
        assert results is not None
        assert results.beat_results is not None
        assert results.pitch_results is not None

        print(len(results.beat_results))
        print(len(results.pitch_results))
        assert 1 == len(results.beat_results)
        assert 1 == len(results.pitch_results)

        new_line = results.apply(next(iter(results.beat_results)), next(iter(results.pitch_results)))
        assert new_line is not None

        print(new_line)
        all_notes = new_line.get_all_notes()
        assert 'C:5' == str(all_notes[0].diatonic_pitch)
        assert 'D:5' == str(all_notes[1].diatonic_pitch)
        assert 'E:5' == str(all_notes[2].diatonic_pitch)
        assert 'F:5' == str(all_notes[3].diatonic_pitch)
        assert 'E:5' == str(all_notes[4].diatonic_pitch)
        assert 'D:5' == str(all_notes[5].diatonic_pitch)

        assert Position(3, 4) == all_notes[1].get_absolute_position()
