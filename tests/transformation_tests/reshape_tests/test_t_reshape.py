import unittest

import logging
from fractions import Fraction

from function.generic_univariate_pitch_function import GenericUnivariatePitchFunction
from function.piecewise_linear_function import PiecewiseLinearFunction
from function.scalar_range_interpreter import ScalarRangeInterpreter
from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.chord_template import ChordTemplate
from instruments.instrument_catalog import InstrumentCatalog
from melody.constraints.chordal_pitch_constraint import ChordalPitchConstraint
from melody.constraints.on_beat_constraint import OnBeatConstraint
from melody.constraints.pitch_range_constraint import PitchRangeConstraint
from melody.constraints.step_sequence_constraint import StepSequenceConstraint
from melody.structure.melodic_form import MelodicForm
from melody.structure.motif import Motif
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.line import Line
from structure.lite_score import LiteScore
from structure.note import Note
from structure.tempo import Tempo
from structure.time_signature import TimeSignature, BeatType
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.range import Range
from tonalmodel.tonality import Tonality
from transformation.reshape.t_reshape import TReshape


import math


class TestTReshape(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_reshape(self):
        print('----- test_hct_simple_shift -----')

        s_notes = [
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),

            ('E:4', 'h'),
            ('E:4', 'h'),

            ('E:4', 'q'),
            ('E:4', 'q'),
            ('E:4', 'q'),
            ('E:4', 'q'),
        ]
        chords = [('tI', 1), ('tIV', (1, 2)), ('tV', (1, 2)), ('tVI', 1)]

        score = TestTReshape.create_score(s_notes, ModalityType.Major, 'C', chords, 'violin', (3, 4, 'sww'))

        all_notes = score.line.get_all_notes()

        pitch_function = GenericUnivariatePitchFunction(TestTReshape.sinasoidal, Position(0), Position(3))
        time_range = Range(0, 3)

        # The first note should have one of 3 values, C:4, E:4, G:4
        constraints = {
            ChordalPitchConstraint(all_notes[0]),
            PitchRangeConstraint([all_notes[0]], PitchRange.create('C:4', 'G:4')),
        }

        motif = Motif(score.line, constraints, 'A')
        melodic_form = MelodicForm([motif])
        treshape = TReshape(score, pitch_function, time_range, melodic_form, False)

        results = treshape.apply()
        assert results is not None
        assert len(results) == 3
        for result in results:
            print('-----')
            print(result.line)

        first_pitch_set = {str(result.line.get_all_notes()[0].diatonic_pitch) for result in results}
        assert {'E:4', 'C:4', 'G:4'} == first_pitch_set

        assert abs(TestTReshape.sinasoidal(Fraction(1, 8)) - DiatonicPitch.parse('D:5').chromatic_distance) < 1

    def test_linear_scale(self):
        print('----- test_linear_scale -----')

        s_notes = [
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
        ]
        chords = [('tI', 1), ('tIV', (1, 2)), ('tV', (1, 2)), ('tVI', 1)]

        score = TestTReshape.create_score(s_notes, ModalityType.Major, 'Eb', chords, 'violin', (3, 4, 'sww'))
        all_notes = score.line.get_all_notes()

        eflat_interp = ScalarRangeInterpreter(Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('Eb')),
                                              'Eb:4', 0)
        pitch_function = GenericUnivariatePitchFunction(TestTReshape.e_flat_linear, Position(0), Position(1), False,
                                                        eflat_interp)
        time_range = Range(0, 3)

        # The first note should have one of 2 values, Eb:4, G:4
        constraints = {
            ChordalPitchConstraint(all_notes[0]),
            PitchRangeConstraint([all_notes[0]], PitchRange.create('C:4', 'G:4')),
        }

        motif = Motif(score.line, constraints, 'A')

        melodic_form = MelodicForm([motif])

        treshape = TReshape(score, pitch_function, time_range, melodic_form)

        results = treshape.apply()
        assert results is not None
        assert len(results) == 2
        for result in results:
            print('-----')
            print(result.line)

        first_pitch_set = {str(result.line.get_all_notes()[0].diatonic_pitch) for result in results}
        assert {'Eb:4', 'G:4'} == first_pitch_set

        all_notes = results[0].line.get_all_notes()
        assert 'F:4' == str(all_notes[1].diatonic_pitch)
        assert 'G:4' == str(all_notes[2].diatonic_pitch)
        assert 'Ab:4' == str(all_notes[3].diatonic_pitch)
        assert 'Bb:4' == str(all_notes[4].diatonic_pitch)
        assert 'C:5' == str(all_notes[5].diatonic_pitch)
        assert 'D:5' == str(all_notes[6].diatonic_pitch)
        assert 'Eb:5' == str(all_notes[7].diatonic_pitch)

        all_notes = results[1].line.get_all_notes()
        assert 'F:4' == str(all_notes[1].diatonic_pitch)
        assert 'G:4' == str(all_notes[2].diatonic_pitch)
        assert 'Ab:4' == str(all_notes[3].diatonic_pitch)
        assert 'Bb:4' == str(all_notes[4].diatonic_pitch)
        assert 'C:5' == str(all_notes[5].diatonic_pitch)
        assert 'D:5' == str(all_notes[6].diatonic_pitch)
        assert 'Eb:5' == str(all_notes[7].diatonic_pitch)

    def test_onbeat_shape(self):
        print('----- test_onbeat_shape -----')

        s_notes = [
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
        ]
        chords = [('tI', 1), ('tIV', (1, 2)), ('tV', (1, 2)), ('tVI', 1)]

        score = TestTReshape.create_score(s_notes, ModalityType.Major, 'Bb', chords, 'violin', (4, 4, 'swww'))
        all_notes = score.line.get_all_notes()

        # The first note should have one of 2 values, Eb:4, G:4
        constraints = {
            ChordalPitchConstraint(all_notes[0]),
            OnBeatConstraint(all_notes[2], BeatType.Strong),
            # You need this kind of constraint to limit possibilities.
            PitchRangeConstraint([all_notes[0]], PitchRange.create('Bb:3', 'A:4')),
        }

        motif = Motif(score.line, constraints, 'A')

        melodic_form = MelodicForm([motif])

        eflat_interp = ScalarRangeInterpreter(Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('Bb')),
                                              'Bb:3', 0)
        pitch_function = GenericUnivariatePitchFunction(TestTReshape.e_flat_linear, Position(0), Position(1), False,
                                                        eflat_interp)
        time_range = Range(0, 3)

        treshape = TReshape(score, pitch_function, time_range, melodic_form, False)

        results = treshape.apply()
        assert results is not None
        for i in range(0, len(results)):
            print('--- result[{0}] ---'.format(i))
            print(results[i].line)

        first_pitch_set = {str(result.line.get_all_notes()[0].diatonic_pitch) for result in results}
        assert {'Bb:3', 'D:4', 'F:4'} == first_pitch_set

        all_notes = results[0].line.get_all_notes()
        assert 'C:4' == str(all_notes[1].diatonic_pitch)
        assert 'C:5' == str(all_notes[2].diatonic_pitch)
        assert 'D:5' == str(all_notes[3].diatonic_pitch)
        assert 'Eb:5' == str(all_notes[4].diatonic_pitch)
        assert 'F:5' == str(all_notes[5].diatonic_pitch)
        assert 'G:5' == str(all_notes[6].diatonic_pitch)
        assert 'A:5' == str(all_notes[7].diatonic_pitch)
        assert Position(1) == all_notes[2].get_absolute_position()

        all_notes = results[1].line.get_all_notes()
        assert 'C:4' == str(all_notes[1].diatonic_pitch)
        assert 'C:5' == str(all_notes[2].diatonic_pitch)
        assert 'D:5' == str(all_notes[3].diatonic_pitch)
        assert 'Eb:5' == str(all_notes[4].diatonic_pitch)
        assert 'F:5' == str(all_notes[5].diatonic_pitch)
        assert 'G:5' == str(all_notes[6].diatonic_pitch)
        assert 'A:5' == str(all_notes[7].diatonic_pitch)
        assert Position(1) == all_notes[2].get_absolute_position()

    def test_pitch_sequence_shape(self):
        print('----- test_pitch_sequence_shape -----')

        s_notes = [
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),

            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
        ]
        chords = [('tI', 1), ('tIV', 1), ('tV', 1), ('tVI', 1)]

        score = TestTReshape.create_score(s_notes, ModalityType.Major, 'Bb', chords, 'violin', (4, 4, 'swww'))
        all_notes = score.line.get_all_notes()

        eflat_interp = ScalarRangeInterpreter(Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('Bb')),
                                              'Bb:3', 0)
        pitch_function = GenericUnivariatePitchFunction(TestTReshape.e_flat_linear, Position(0), Position(1), False,
                                                        eflat_interp)

        # The first note should have one of 2 values, Eb:4, G:4
        constraints = {
            ChordalPitchConstraint(all_notes[0]),
            # You need this kind of constraint to limit possibilities.
            PitchRangeConstraint([all_notes[0]], PitchRange.create('Bb:3', 'A:4')),
            StepSequenceConstraint([all_notes[3], all_notes[4], all_notes[5], all_notes[6]], [-1, -1, -1]),
        }

        motif = Motif(score.line, constraints, 'A')

        melodic_form = MelodicForm([motif])

        time_range = Range(0, 3)

        treshape = TReshape(score, pitch_function, time_range, melodic_form, True)
        results = treshape.apply()
        assert results is not None
        for i in range(0, len(results)):
            print('--- result[{0}] ---'.format(i))
            print(results[i].line)

        for result in results:
            notes = result.line.get_all_notes()
            if str(notes[3].diatonic_pitch) == 'Eb:4':
                assert 'D:4' == str(notes[4].diatonic_pitch)
                assert 'C:4' == str(notes[5].diatonic_pitch)
                assert 'Bb:3' == str(notes[6].diatonic_pitch)
            else:
                assert 'D:4' == str(notes[3].diatonic_pitch)
                assert 'C:4' == str(notes[4].diatonic_pitch)
                assert 'Bb:3' == str(notes[5].diatonic_pitch)
                assert 'A:3' == str(notes[6].diatonic_pitch)

    def test_piecewise_linear_reshape(self):
        """
        This is a very interesting test case. Although it uses a piecewise linear based reshape function, more
        importantly, the line's harmonic context track is in the key Bb-major, but the pitch function interprets
        pitches in E-major!
        The rule is to always use what the pitch function returns over the hct, except when the computed pitch has
        an enharmonic equivalent - in this case, the only case is Eb == D#, and Eb is preferred.
        :return:
        """
        print('----- test_piecewise_linear_reshape -----')

        s_notes = [
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),

            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
            ('E:4', 'e'),
        ]
        chords = [('tI', 1), ('tIV', (1, 2)), ('tV', (1, 2)), ('tVI', 1)]

        score = TestTReshape.create_score(s_notes, ModalityType.Major, 'Bb', chords, 'violin', (4, 4, 'swww'))

        e_interp = ScalarRangeInterpreter(Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('E')), 'E:4',
                                          0)

        array = [(0, 0), (Fraction(1, 2), 4), (Fraction(1), 0), (Fraction(2), 8)]
        f = PiecewiseLinearFunction(array)
        pitch_function = GenericUnivariatePitchFunction(f, Position(0), Position(2), False,
                                                        e_interp)
        all_notes = score.line.get_all_notes()

        # The first note should have one of 2 values, Eb:4, G:4
        constraints = {
            ChordalPitchConstraint(all_notes[0]),
        }

        motif = Motif(score.line, constraints, 'A')

        melodic_form = MelodicForm([motif])

        time_range = Range(0, 3)

        treshape = TReshape(score, pitch_function, time_range, melodic_form, True)
        results = treshape.apply()
        assert results is not None
        for i in range(0, len(results)):
            print('--- result[{0}] ---'.format(i))
            print(results[i].line)

        assert len(results) == 2
        first_pitch_set = {str(result.line.get_all_notes()[0].diatonic_pitch) for result in results}
        assert {'D:4', 'F:4'} == first_pitch_set

        all_notes = results[0].line.get_all_notes()
        assert 'F#:4' == str(all_notes[1].diatonic_pitch)
        assert 'G#:4' == str(all_notes[2].diatonic_pitch)
        assert 'A:4' == str(all_notes[3].diatonic_pitch)
        assert 'B:4' == str(all_notes[4].diatonic_pitch)
        assert 'A:4' == str(all_notes[5].diatonic_pitch)
        assert 'G#:4' == str(all_notes[6].diatonic_pitch)
        assert 'F#:4' == str(all_notes[7].diatonic_pitch)
        assert 'E:4' == str(all_notes[8].diatonic_pitch)
        assert 'F#:4' == str(all_notes[9].diatonic_pitch)
        assert 'G#:4' == str(all_notes[10].diatonic_pitch)
        assert 'A:4' == str(all_notes[11].diatonic_pitch)
        assert 'B:4' == str(all_notes[12].diatonic_pitch)
        assert 'C#:5' == str(all_notes[13].diatonic_pitch)
        assert 'Eb:5' == str(all_notes[14].diatonic_pitch)

        all_notes = results[1].line.get_all_notes()
        assert 'F#:4' == str(all_notes[1].diatonic_pitch)
        assert 'G#:4' == str(all_notes[2].diatonic_pitch)
        assert 'A:4' == str(all_notes[3].diatonic_pitch)
        assert 'B:4' == str(all_notes[4].diatonic_pitch)
        assert 'A:4' == str(all_notes[5].diatonic_pitch)
        assert 'G#:4' == str(all_notes[6].diatonic_pitch)
        assert 'F#:4' == str(all_notes[7].diatonic_pitch)
        assert 'E:4' == str(all_notes[8].diatonic_pitch)
        assert 'F#:4' == str(all_notes[9].diatonic_pitch)
        assert 'G#:4' == str(all_notes[10].diatonic_pitch)
        assert 'A:4' == str(all_notes[11].diatonic_pitch)
        assert 'B:4' == str(all_notes[12].diatonic_pitch)
        assert 'C#:5' == str(all_notes[13].diatonic_pitch)
        assert 'Eb:5' == str(all_notes[14].diatonic_pitch)

    BASE = DiatonicPitch.parse('C:4').chromatic_distance

    @staticmethod
    def sinasoidal(v):
        """
        Maps v to a chromatic distance.
        :param v:
        :return:
        [0..1] -->[0..2*PI]-->[0..19] with value added to C:4 absolute chromatic distance.
        """
        return TestTReshape.BASE + 19 * math.sin(2 * math.pi * v)

    @staticmethod
    def e_flat_linear(v):
        return 8 * v

    @staticmethod
    def create_track(chords, tonality):
        hc_track = HarmonicContextTrack()
        for c in chords:
            chord_t = ChordTemplate.generic_chord_template_parse(c[0])
            chord = chord_t.create_chord(tonality)
            duration = Duration(c[1]) if isinstance(c[1], int) else Duration(c[1][0], c[1][1])
            hc_track.append(HarmonicContext(tonality, chord, duration))
        return hc_track

    @staticmethod
    def create_line(note_spec_list):
        note_list = list()
        for spec in note_spec_list:
            pitch = DiatonicPitch.parse(spec[0])
            if isinstance(spec[1], str):
                s_d = spec[1].upper()
                if s_d == 'Q':
                    d = Duration(1, 4)
                elif s_d == 'H':
                    d = Duration(1, 2)
                elif s_d == 'W':
                    d = Duration(1)
                elif s_d == 'E':
                    d = Duration(1, 8)
                elif s_d == 'S':
                    d = Duration(1, 16)
                else:
                    d = Duration(1, 4)
            else:
                d = Duration(spec[1][0], spec[1][1])
            n = Note(pitch, d)
            note_list.append(n)
        return Line(note_list)

    @staticmethod
    def create_score(s_notes, modality, key_tone, chords, instrument, ts):
        diatonic_tonality = Tonality.create(modality, DiatonicToneCache.get_tone(key_tone))

        hc_track = TestTReshape.create_track(chords, diatonic_tonality)

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(ts[0], Duration(1, ts[1]), ts[2]), Position(0)))

        c = InstrumentCatalog.instance()
        violin = c.get_instrument(instrument)

        return LiteScore(TestTReshape.create_line(s_notes), hc_track, violin, tempo_seq, ts_seq)
