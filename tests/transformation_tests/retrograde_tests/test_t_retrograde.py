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
from transformation.retrograde.t_retrograde import TRetrograde
from misc.interval import Interval as NumericInterval, BoundaryPolicy


class TestTRetrograde(unittest.TestCase):
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_melodic_reversal(self):
        print('----- test simple melodic reversal -----')

        source_instance_expression = '{<C-Major:I> qC:4 D E G <:v> [iD:5 B:4 A G] qC:5 D <:IV> A:4 iF E hC}'

        lite_score = TestTRetrograde.create_score(source_instance_expression, 'piano', (4, 4, 'swww'))

        trans = TRetrograde(lite_score)

        print('--- With harmonic reversal ---')
        reversed_line, hct = trans.apply()

        print(str(reversed_line))
        print(str(hct))

        score_notes = lite_score.line.get_all_notes()
        reversed_line_notes = reversed_line.get_all_notes()
        assert len(score_notes) == len(reversed_line_notes)
        for i in range(0, len(score_notes)):
            if score_notes[i].diatonic_pitch != reversed_line_notes[-1 - i].diatonic_pitch:
                assert score_notes[i].diatonic_pitch == reversed_line_notes[-1 - i], 'score note {0} invalid'.format(i)

        score_hct_list = lite_score.hct.hc_list()
        hct_list = hct.hc_list()
        assert len(hct_list) == 3
        assert len(score_hct_list) == 3
        assert hct_list[0].is_equal(score_hct_list[2])
        assert hct_list[1].is_equal(score_hct_list[1])
        assert hct_list[2].is_equal(score_hct_list[0])

        # Reverse harmony
        print('--- No harmonic reversal - original harmony ---')
        reversed_line, hct = trans.apply(False)

        print(str(reversed_line))
        print(str(hct))

        score_hct_list = lite_score.hct.hc_list()
        hct_list = hct.hc_list()
        assert len(hct_list) == 3
        assert len(score_hct_list) == 3
        assert hct_list[0].is_equal(score_hct_list[0])
        assert hct_list[1].is_equal(score_hct_list[1])
        assert hct_list[2].is_equal(score_hct_list[2])

    def test_sub_line_reversal(self):
        print('----- test sub line reversal -----')

        source_instance_expression = '{<C-Major:I> qC:4 D E F <:v> [iD:5 B:4 A G] qC:5 D <:IV> A:4 iF E hC}'

        lite_score = TestTRetrograde.create_score(source_instance_expression, 'piano', (4, 4, 'swww'))

        trans = TRetrograde(lite_score)

        print('--- With sub_line harmonic reversal ---')
        reversed_line, hct = trans.apply(True, NumericInterval(Fraction(1, 2), Fraction(9, 4), BoundaryPolicy.Closed))

        print(str(lite_score.line))
        print(str(lite_score.hct))
        print(str(reversed_line))
        print(str(hct))

        score_hct_list = lite_score.hct.hc_list()
        hct_list = hct.hc_list()
        assert len(hct_list) == 3
        assert len(score_hct_list) == 3
        assert hct_list[0].is_same_harmony(score_hct_list[2])
        assert hct_list[1].is_equal(score_hct_list[1])
        assert hct_list[2].is_same_harmony(score_hct_list[0])

        assert hct_list[0].duration == Duration(3, 8)
        assert hct_list[1].duration == Duration(1)
        assert hct_list[2].duration == Duration(1, 2)

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
