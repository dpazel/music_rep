import unittest
import logging
from fractions import Fraction

from instruments.instrument_catalog import InstrumentCatalog
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.lite_score import LiteScore
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from timemodel.offset import Offset
from transformation.dilation.t_dilation import TDilation

from structure.line import Line


class TestTDilation(unittest.TestCase):
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_dilation(self):
        print('----- test simple dilation -----')

        source_instance_expression = '{<C-Major:I> qC:4 D <D-Major:ii> E G}'

        lite_score = TestTDilation.create_score(source_instance_expression, 'piano', (4, 4, 'swww'))

        trans = TDilation(lite_score)

        #  case 0: apply_to_bpm=False apply_to_notes=True
        new_score = trans.apply(Fraction(2), False, True)

        new_line = new_score.line
        notes = new_line.get_all_notes()
        n = notes[0]
        assert n is not None
        assert n.duration == Duration(Fraction(1, 2))

        tempo_sequence = new_score.tempo_sequence.sequence_list
        tempo = tempo_sequence[0].object
        assert tempo is not None
        assert tempo.tempo == 60
        assert tempo.beat_duration == Duration(Fraction(1, 2))

        time_sequence = new_score.time_signature_sequence.sequence_list
        ts = time_sequence[0].object
        assert ts is not None
        assert ts.beats_per_measure == 4
        assert ts.beat_duration == Duration(Fraction(1, 2))

        new_hct = new_score.hct
        hct_list = new_hct.hc_list()
        hc = hct_list[0]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 1))
        hc = hct_list[1]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 1))
        assert hc.position == Position(Fraction(1))

        #  case 1: apply_to_bpm=True apply_to_notes=False
        new_score = trans.apply(Fraction(2), True, True)

        new_line = new_score.line
        notes = new_line.get_all_notes()
        n = notes[0]
        assert n is not None
        assert n.duration == Duration(Fraction(1, 2))

        tempo_sequence = new_score.tempo_sequence.sequence_list
        tempo = tempo_sequence[0].object
        assert tempo is not None
        assert tempo.tempo == 30
        assert tempo.beat_duration == Duration(Fraction(1, 2))

        time_sequence = new_score.time_signature_sequence.sequence_list
        ts = time_sequence[0].object
        assert ts is not None
        assert ts.beats_per_measure == 4
        assert ts.beat_duration == Duration(Fraction(1, 2))

        new_hct = new_score.hct
        hct_list = new_hct.hc_list()
        hc = hct_list[0]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 1))
        hc = hct_list[1]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 1))
        assert hc.position == Position(Fraction(1))

        #  case 2: apply_to_bpm=False apply_to_notes=False
        new_score = trans.apply(Fraction(2), False, False)

        new_line = new_score.line
        notes = new_line.get_all_notes()
        n = notes[0]
        assert n is not None
        assert n.duration == Duration(Fraction(1, 4))

        tempo_sequence = new_score.tempo_sequence.sequence_list
        tempo = tempo_sequence[0].object
        assert tempo is not None
        assert tempo.tempo == 60
        assert tempo.beat_duration == Duration(Fraction(1, 4))

        time_sequence = new_score.time_signature_sequence.sequence_list
        ts = time_sequence[0].object
        assert ts is not None
        assert ts.beats_per_measure == 4
        assert ts.beat_duration == Duration(Fraction(1, 4))

        new_hct = new_score.hct
        hct_list = new_hct.hc_list()
        hc = hct_list[0]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 2))
        hc = hct_list[1]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 2))
        assert hc.position == Position(Fraction(1, 2))

        #  case 3: apply_to_bpm=True apply_to_notes=Flase
        new_score = trans.apply(Fraction(2), True, False)

        new_line = new_score.line
        notes = new_line.get_all_notes()
        n = notes[0]
        assert n is not None
        assert n.duration == Duration(Fraction(1, 4))

        tempo_sequence = new_score.tempo_sequence.sequence_list
        tempo = tempo_sequence[0].object
        assert tempo is not None
        assert tempo.tempo == 30
        assert tempo.beat_duration == Duration(Fraction(1, 4))

        time_sequence = new_score.time_signature_sequence.sequence_list
        ts = time_sequence[0].object
        assert ts is not None
        assert ts.beats_per_measure == 4
        assert ts.beat_duration == Duration(Fraction(1, 4))

        new_hct = new_score.hct
        hct_list = new_hct.hc_list()
        hc = hct_list[0]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 2))
        hc = hct_list[1]
        assert hc is not None
        assert hc.duration == Duration(Fraction(1, 2))
        assert hc.position == Position(Fraction(1, 2))

        print(new_score)

    def test_structures(self):
        print('----- test structures -----')

        source_instance_expression = '{<C-Major:I> [[[sE F G A] iC D]} }'

        lite_score = TestTDilation.create_score(source_instance_expression, 'piano', (4, 4, 'swww'))

        trans = TDilation(lite_score)

        new_score = trans.apply(Fraction(2), False, True)

        print(new_score.line)
        new_line = new_score.line
        notes = new_line.get_all_notes()
        n = notes[0]
        assert n is not None
        assert n.duration == Duration(Fraction(1, 32))

        source_instance_expression = '{<C-Major:I>(i, 2)[iC:3 D:4 E] }'

        lite_score = TestTDilation.create_score(source_instance_expression, 'piano', (4, 4, 'swww'))

        trans = TDilation(lite_score)

        new_score = trans.apply(Fraction(2), False, True)

        print(new_score.line)
        new_line = new_score.line
        notes = new_line.get_all_notes()
        n = notes[0]
        assert n is not None
        assert n.duration == Duration(Fraction(1, 6))

    def test_line_structures(self):
        print('----- test line structures -----')
        source_instance_expression = '{<C-Major:I> iC:4 D E F G A B C:5 D E F G} }'
        lge = LineGrammarExecutor()
        source_instance_line, source_instance_hct = lge.parse(source_instance_expression)
        notes = source_instance_line.get_all_notes()

        line = Line()
        line.pin(notes[0], Offset(Fraction(1, 2)))
        line.pin(notes[1], Offset(Fraction(3, 4)))

        line1 = Line()
        line1.pin(notes[3], Offset(Fraction(1, 4)))
        line1.pin(notes[4], Offset(Fraction(1, 2)))
        line.pin(line1, Offset(Fraction(2)))

        lite_score = TestTDilation.create_score_1(line, source_instance_hct, 'piano', (4, 4, 'swww'))

        trans = TDilation(lite_score)
        new_score = trans.apply(Fraction(2), False, True)
        all_notes = new_score.line.get_all_notes()
        assert all_notes[2].get_absolute_position().position == Fraction(9, 2)

        print(line)
        print(new_score.line)

    @staticmethod
    def create_score(line_expression, instrument, ts):
        lge = LineGrammarExecutor()
        source_instance_line, source_instance_hct = lge.parse(line_expression)

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(ts[0], Duration(1, ts[1]), ts[2]), Position(0)))

        c = InstrumentCatalog.instance()
        instrument = c.get_instrument(instrument)

        return LiteScore(source_instance_line, source_instance_hct, instrument, tempo_seq, ts_seq)

    @staticmethod
    def create_score_1(line, hct, instrument, ts):
        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(ts[0], Duration(1, ts[1]), ts[2]), Position(0)))

        c = InstrumentCatalog.instance()
        instrument = c.get_instrument(instrument)

        return LiteScore(line, hct, instrument, tempo_seq, ts_seq)

