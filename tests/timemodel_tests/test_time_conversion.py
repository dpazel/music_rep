import unittest
from timemodel.time_conversion import TimeConversion
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.position import Position
from timemodel.duration import Duration
from timemodel.beat_position import BeatPosition

from timemodel.tempo_event import TempoEvent
from timemodel.time_signature_event import TimeSignatureEvent
from timemodel.event_sequence import EventSequence


class TestTimeConversion(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_time_conversion_simple(self):
        tempo_line = EventSequence([TempoEvent(Tempo(60), Position(0))])
        ts_line = EventSequence([TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0))])
        conversion = TimeConversion(tempo_line, ts_line, Position(1, 1))
        actual_time = conversion.position_to_actual_time(Position(3, 4))
        print actual_time
        self.assertTrue(actual_time == 3000, 'actual time = {0} should be 3000'.format(actual_time))
        
        position = conversion.actual_time_to_position(3000)
        print position
        self.assertTrue(position, Position(3, 4))
        
    def test_position_to_actual_time(self):
        tempo_line = EventSequence([TempoEvent(Tempo(60), Position(0)), TempoEvent(Tempo(20), Position(4, 4))])
        ts_line = EventSequence([TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)),
                                 TimeSignatureEvent(TimeSignature(2, Duration(1, 8)), Position(5, 4))])
        conversion = TimeConversion(tempo_line, ts_line, Position(2, 1))
        actual_time = conversion.position_to_actual_time(Position(6, 4))
        print actual_time
        # 4 quarter notes @ 60 with 1/4 beat = 4000
        # 1 quarter note @ 20 with 1/4 beat  = 3000
        # 2 eighth notes @ 20 (effective 40) with 1/8 beat  = 3000
        self.assertTrue(actual_time == 10000, 'actual time = {0} should be 10000'.format(actual_time))
        
        position = conversion.actual_time_to_position(13000)
        print position
        self.assertTrue(position, Position(6, 4))
        
    def test_bp_to_position(self):
        tempo_line = EventSequence([TempoEvent(Tempo(60), Position(0))])
        ts_line = EventSequence(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        conversion = TimeConversion(tempo_line, ts_line, Position(2, 1))
        
        bp = conversion.bp_to_position(BeatPosition(0, 2))
        print bp
        self.assertTrue(bp == Position(1, 2), 'bp is {0}, not 1/2'.format(bp))   
        
        bp = conversion.bp_to_position(BeatPosition(1, 1))
        print bp
        self.assertTrue(bp == Position(1), 'bp is {0}, not 1'.format(bp))    

        tempo_line = EventSequence([TempoEvent(Tempo(60), Position(0)), TempoEvent(Tempo(20), Position(4, 4))])
        ts_line = EventSequence([TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)),
                                 TimeSignatureEvent(TimeSignature(2, Duration(1, 8)), Position(6, 4))])
        conversion = TimeConversion(tempo_line, ts_line, Position(2, 1))
        
        bp = conversion.bp_to_position(BeatPosition(1, 2))
        print bp
        self.assertTrue(bp == Position(5, 4), 'bp is {0}, not 5/4'.format(bp))      
        
        bp = conversion.bp_to_position(BeatPosition(2, 1))
        print bp
        self.assertTrue(bp == Position(13, 8), 'bp is {0}, not 13/8'.format(bp))  

        tempo_line = EventSequence([TempoEvent(Tempo(60), Position(0)), TempoEvent(Tempo(20), Position(4, 4))])
        ts_line = EventSequence([TimeSignatureEvent(TimeSignature(4, Duration(1, 4)), Position(0)),
                                 TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(5, 2))])
        conversion = TimeConversion(tempo_line, ts_line, Position(4), Duration(1, 2))        
        
        # pickup
        bp = conversion.bp_to_position(BeatPosition(0, 2))
        print bp
        self.assertTrue(bp == Position(0), 'bp is {0}, not 0'.format(bp))  
        
        bp = conversion.bp_to_position(BeatPosition(0, 3))
        print bp
        self.assertTrue(bp == Position(1, 4), 'bp is {0}, not 1/4'.format(bp))  
        
        # measure 1
        bp = conversion.bp_to_position(BeatPosition(1, 0))
        print bp
        self.assertTrue(bp == Position(1, 2), 'bp is {0}, not 1/2'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(1, 1))
        print bp
        self.assertTrue(bp == Position(3, 4), 'bp is {0}, not 3/4'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(1, 2))
        print bp
        self.assertTrue(bp == Position(1, 1), 'bp is {0}, not 1'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(1, 3))
        print bp
        self.assertTrue(bp == Position(5, 4), 'bp is {0}, not 5/4'.format(bp)) 
        
        # measure 2
        bp = conversion.bp_to_position(BeatPosition(2, 0))
        print bp
        self.assertTrue(bp == Position(3, 2), 'bp is {0}, not 3/2'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(2, 1))
        print bp
        self.assertTrue(bp == Position(7, 4), 'bp is {0}, not 7/4'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(2, 2))
        print bp
        self.assertTrue(bp == Position(2, 1), 'bp is {0}, not 2'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(2, 3))
        print bp
        self.assertTrue(bp == Position(9, 4), 'bp is {0}, not 9/4'.format(bp)) 
        
        # measure 3
        bp = conversion.bp_to_position(BeatPosition(3, 0))
        print bp
        self.assertTrue(bp == Position(5, 2), 'bp is {0}, not 5/2'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(3, 1))
        print bp
        self.assertTrue(bp == Position(11, 4), 'bp is {0}, not 11/4'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(3, 2))
        print bp
        self.assertTrue(bp == Position(3, 1), 'bp is {0}, not 3'.format(bp)) 
        
        # measure 4
        bp = conversion.bp_to_position(BeatPosition(4, 0))
        print bp
        self.assertTrue(bp == Position(13, 4), 'bp is {0}, not 13/4'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(4, 1))
        print bp
        self.assertTrue(bp == Position(7, 2), 'bp is {0}, not 7, 2'.format(bp)) 
        
        bp = conversion.bp_to_position(BeatPosition(4, 2))
        print bp
        self.assertTrue(bp == Position(15, 4), 'bp is {0}, not 15/4'.format(bp)) 
        
    def test_position_to_bp(self):
        tempo_line = EventSequence(TempoEvent(Tempo(60), Position(0)))
        ts_line = EventSequence(TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)))
        conversion = TimeConversion(tempo_line, ts_line, Position(2, 1))
        
        bp = conversion.position_to_bp(Position(1, 2))
        print bp
        self.assertTrue(bp == BeatPosition(0, 2), 'bp is {0}, not BP[0, 2]'.format(bp))   
        
        bp = conversion.position_to_bp(Position(1))
        print bp
        self.assertTrue(bp == BeatPosition(1, 1), 'bp is {0}, not BP[1 ,1]'.format(bp))

        tempo_line = EventSequence([TempoEvent(Tempo(60), Position(0)), TempoEvent(Tempo(20), Position(4, 4))])
        ts_line = EventSequence([TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(0)),
                                 TimeSignatureEvent(TimeSignature(2, Duration(1, 8)), Position(6, 4))])
        conversion = TimeConversion(tempo_line, ts_line, Position(2, 1))
        
        bp = conversion.position_to_bp(Position(5, 4))
        print bp
        self.assertTrue(bp == BeatPosition(1, 2), 'bp is {0}, not BP[1, 2]'.format(bp))      
        
        bp = conversion.position_to_bp(Position(13, 8))
        print bp
        self.assertTrue(bp == BeatPosition(2, 1), 'bp is {0}, not BP[2, 1]'.format(bp))  

        tempo_line = EventSequence([TempoEvent(Tempo(60), Position(0)), TempoEvent(Tempo(20), Position(4, 4))])
        ts_line = EventSequence([TimeSignatureEvent(TimeSignature(4, Duration(1, 4)), Position(0)),
                                 TimeSignatureEvent(TimeSignature(3, Duration(1, 4)), Position(5, 2))])
        conversion = TimeConversion(tempo_line, ts_line, Position(4), Duration(1, 2))        
        
        # pickup
        bp = conversion.position_to_bp(Position(0))
        print bp
        self.assertTrue(bp == BeatPosition(0, 2), 'bp is {0}, not BP[0, 2]'.format(bp))  
        
        bp = conversion.position_to_bp(Position(1, 4))
        print bp
        self.assertTrue(bp == BeatPosition(0, 3), 'bp is {0}, not BP[0, 3]'.format(bp))  
        
        # measure 1
        bp = conversion.position_to_bp(Position(1, 2))
        print bp
        self.assertTrue(bp == BeatPosition(1, 0), 'bp is {0}, not BP[1, 0]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(3, 4))
        print bp
        self.assertTrue(bp == BeatPosition(1, 1), 'bp is {0}, not BP[1, 1]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(1, 1))
        print bp
        self.assertTrue(bp == BeatPosition(1, 2), 'bp is {0}, not BP[1, 2]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(5, 4))
        print bp
        self.assertTrue(bp == BeatPosition(1, 3), 'bp is {0}, not BP[1, 3]'.format(bp)) 
               
        # measure 2
        bp = conversion.position_to_bp(Position(3, 2))
        print bp
        self.assertTrue(bp == BeatPosition(2, 0), 'bp is {0}, not BP[2, 0]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(7, 4))
        print bp
        self.assertTrue(bp == BeatPosition(2, 1), 'bp is {0}, not BP[2, 1]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(2, 1))
        print bp
        self.assertTrue(bp == BeatPosition(2, 2), 'bp is {0}, not BP[2, 2]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(9, 4))
        print bp
        self.assertTrue(bp == BeatPosition(2, 3), 'bp is {0}, not BP[2, 3]'.format(bp)) 
        
        # measure 3
        bp = conversion.position_to_bp(Position(5, 2))
        print bp
        self.assertTrue(bp == BeatPosition(3, 0), 'bp is {0}, not TS[3, 0]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(11, 4))
        print bp
        self.assertTrue(bp == BeatPosition(3, 1), 'bp is {0}, not TS[3, 1]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(3, 1))
        print bp
        self.assertTrue(bp == BeatPosition(3, 2), 'bp is {0}, not TS[3, 2]'.format(bp)) 
        
        # measure 4
        bp = conversion.position_to_bp(Position(13, 4))
        print bp
        self.assertTrue(bp == BeatPosition(4, 0), 'bp is {0}, not BP[4, 0]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(7, 2))
        print bp
        self.assertTrue(bp == BeatPosition(4, 1), 'bp is {0}, not BP[4, 1]'.format(bp)) 
        
        bp = conversion.position_to_bp(Position(15, 4))
        print bp
        self.assertTrue(bp == BeatPosition(4, 2), 'bp is {0}, not BP[4, 2]'.format(bp)) 

if __name__ == "__main__":
    unittest.main()
