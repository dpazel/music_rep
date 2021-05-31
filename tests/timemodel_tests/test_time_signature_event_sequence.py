import unittest
from timemodel.time_signature_event_sequence import TimeSignatureEventSequence
from timemodel.tempo_function_event import TempoFunctionEvent

from timemodel.position import Position
from timemodel.time_signature_event import TimeSignatureEvent
from structure.time_signature import TimeSignature, TSBeatType


class TestTimeSignatureEventSequence(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_book_example(self):
        print('----- test_book_example -----')

        seq = TimeSignatureEventSequence()
        seq.add(TimeSignatureEvent(TimeSignature(3, TSBeatType(TSBeatType.Quarter)), Position(0)))
        seq.add(TimeSignatureEvent(TimeSignature(2, TSBeatType(TSBeatType.Half)), Position(10)))
        seq.add(TimeSignatureEvent(TimeSignature(6, TSBeatType(TSBeatType.Eighth)), Position(25)))
        seq.add(TimeSignatureEvent(TimeSignature(3, TSBeatType(TSBeatType.Quarter)), Position(50)))

        event = seq.first
        while event is not None:
            print(event)
            event = seq.successor(event)

        print('----- End test_book_example -----')


