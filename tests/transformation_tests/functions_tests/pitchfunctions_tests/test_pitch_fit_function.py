import logging
import sys
import unittest

from function.generic_univariate_pitch_function import GenericUnivariatePitchFunction
from function.scalar_range_interpreter import ScalarRangeInterpreter
from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.chord_template import ChordTemplate
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from transformation.functions.pitchfunctions.pitch_fit_function import PitchFitFunction


class TestPitchFitFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_pitch_function(self):
        print('--- test_simple_pitch_function ---')
        eflat_interp = ScalarRangeInterpreter(Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('Eb')),
                                              'Eb:4', 0)
        pitch_function = GenericUnivariatePitchFunction(TestPitchFitFunction.e_flat_linear, Position(0), Position(1),
                                                        False,
                                                        eflat_interp)

        chords = [('tI', 1), ('tIV', (1, 2)), ('tV', (1, 2)), ('tVI', 1)]
        hct, tempo_sequence, ts_sequence = TestPitchFitFunction.create_score_artifacts(ModalityType.Major,
                                                                                       'Eb', chords, (4, 4, 'swww'))

        pitch_fit_function = PitchFitFunction(pitch_function, tempo_sequence, ts_sequence, hct)

        p = Position(0)
        d = Duration(1, 16)

        pitches = list()
        for i in range(0, 32):
            pitch = pitch_fit_function(p)
            print('f({0}) = {1}'.format(p, pitch))
            pitches.append(pitch)
            p = p + d

        assert 'Eb:4' == str(pitches[0])
        assert 'F:4' == str(pitches[1])
        assert 'G:4' == str(pitches[2])
        assert 'Ab:4' == str(pitches[3])
        assert 'Bb:4' == str(pitches[4])
        assert 'C:5' == str(pitches[5])
        assert 'D:5' == str(pitches[6])
        assert 'Eb:5' == str(pitches[7])
        assert 'F:5' == str(pitches[8])
        assert 'G:5' == str(pitches[9])

    def test_differing_keys(self):
        print('--- test_differing_keys ---')
        bflat_interp = ScalarRangeInterpreter(Tonality.create(ModalityType.Major, DiatonicToneCache.get_tone('Bb')),
                                              'Bb:3', 0)
        pitch_function = GenericUnivariatePitchFunction(TestPitchFitFunction.e_flat_linear, Position(0), Position(1),
                                                        False,
                                                        bflat_interp)

        chords = [('tI', 1), ('tIV', (1, 2)), ('tV', (1, 2)), ('tVI', 1)]
        hct, tempo_sequence, ts_sequence = TestPitchFitFunction.create_score_artifacts(ModalityType.Major,
                                                                                       'E', chords, (4, 4, 'swww'))

        pitch_fit_function = PitchFitFunction(pitch_function, tempo_sequence, ts_sequence, hct)

        p = Position(0)
        d = Duration(1, 16)

        pitches = list()
        for i in range(0, 32):
            pitch = pitch_fit_function(p)
            print('f({0}) = {1}'.format(p, pitch))
            pitches.append(pitch)
            p = p + d

        assert pitches[0] is None
        assert 'C:4' == str(pitches[1])
        assert 'D:4' == str(pitches[2])
        assert 'D#:4' == str(pitches[3])
        assert 'F:4' == str(pitches[4])
        assert 'G:4' == str(pitches[5])
        assert 'A:4' == str(pitches[6])
        assert 'Bb:4' == str(pitches[7])
        assert 'C:5' == str(pitches[8])
        assert 'D:5' == str(pitches[9])

    @staticmethod
    def e_flat_linear(v):
        return 16 * v

    @staticmethod
    def create_score_artifacts(modality, key_tone, chords, ts):
        diatonic_tonality = Tonality.create(modality, DiatonicToneCache.get_tone(key_tone))

        hc_track = TestPitchFitFunction.create_track(chords, diatonic_tonality)

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(ts[0], Duration(1, ts[1]), ts[2]), Position(0)))

        return hc_track, tempo_seq, ts_seq

    @staticmethod
    def create_track(chords, tonality):
        hc_track = HarmonicContextTrack()
        for c in chords:
            chord_t = ChordTemplate.generic_chord_template_parse(c[0])
            chord = chord_t.create_chord(tonality)
            duration = Duration(c[1]) if isinstance(c[1], int) else Duration(c[1][0], c[1][1])
            hc_track.append(HarmonicContext(tonality, chord, duration))
        return hc_track
