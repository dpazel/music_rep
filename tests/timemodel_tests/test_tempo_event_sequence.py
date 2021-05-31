import unittest
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.tempo_function_event import TempoFunctionEvent
from structure.tempo import Tempo, TempoType

from timemodel.position import Position
from function.piecewise_linear_function import PiecewiseLinearFunction
from function.stepwise_function import StepwiseFunction
from timemodel.tempo_event import TempoEvent


class TestTempoEventSequence(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_sequence(self):
        settings = [Tempo(TempoType.Grave),
                    Tempo(TempoType.Allegrissimo),
                    Tempo(TempoType.Moderato),
                    Tempo(TempoType.Largo),
                    Tempo(TempoType.Vivace),
                    ]
        events = [TempoFunctionEvent(settings[0], Position(0)), 
                  TempoFunctionEvent(settings[1], Position(10)), 
                  TempoFunctionEvent(settings[2], Position(20)), 
                  TempoFunctionEvent(settings[3], Position(40)), 
                  TempoFunctionEvent(settings[4], Position(60)) 
                  ]
        tes = TempoEventSequence(events)
        print(tes)
        
        assert tes.tempo(Position(0)) == settings[0].tempo
        assert tes.tempo(Position(10)) == settings[1].tempo
        assert tes.tempo(Position(20)) == settings[2].tempo
        assert tes.tempo(Position(40)) == settings[3].tempo
        assert tes.tempo(Position(60)) == settings[4].tempo
        
        assert tes.tempo(Position(15)) == settings[1].tempo
        assert tes.tempo(Position(45)) == settings[3].tempo
        
    def test_accel_decel_sequence(self):
        t_low = Tempo(TempoType.Moderato)
        event0 = TempoFunctionEvent(t_low, Position(0))
        
        t_hi = Tempo(TempoType.Vivace)
        array = [(Position(10), t_low.tempo),
                 (Position(30), t_hi.tempo)
                 ]
        f = PiecewiseLinearFunction(array)
        event1 = TempoFunctionEvent(f, Position(10))
        
        event2 = TempoFunctionEvent(t_hi, Position(40))
        
        tes = TempoEventSequence([event0, event1, event2])
        print(tes)

        assert tes.tempo(Position(0)) == t_low.tempo
        assert tes.tempo(Position(10)) == t_low.tempo
        assert tes.tempo(Position(40)) == t_hi.tempo
        
        assert tes.tempo(Position(25)) == (t_low.tempo + t_hi.tempo) / 2.0
        assert tes.tempo(Position(30)) == t_low.tempo + (2 * (t_hi.tempo - t_low.tempo) / 3.0)
        
        assert tes.tempo(Position(50)) == t_hi.tempo
        
        t_hi = Tempo(TempoType.Vivace)
        t_low = Tempo(TempoType.Moderato)
        event0 = TempoFunctionEvent(t_hi, Position(0))
        
        array = [(Position(10), t_hi.tempo),
                 (Position(30), t_low.tempo)]
        f = PiecewiseLinearFunction(array) 
        event1 = TempoFunctionEvent(f, Position(10))
        
        event2 = TempoFunctionEvent(t_low, Position(40)) 
        
        tes = TempoEventSequence([event0, event1, event2])
        print(tes)
        
        assert tes.tempo(Position(0)) == t_hi.tempo
        assert tes.tempo(Position(10)) == t_hi.tempo
        assert tes.tempo(Position(40)) == t_low.tempo
        
        assert tes.tempo(Position(25)) == (t_low.tempo + t_hi.tempo) / 2.0
        assert tes.tempo(Position(30)) == t_hi.tempo - (2 * (t_hi.tempo - t_low.tempo) / 3.0)
        
        assert tes.tempo(Position(50)) == t_low.tempo        
        
    def test_step_wise_tempo(self):
        t_lo_steady = Tempo(TempoType.Grave)
        event0 = TempoEvent(t_lo_steady, Position(0))
        
        settings = [Tempo(TempoType.Grave),
                    Tempo(TempoType.Allegrissimo),
                    Tempo(TempoType.Moderato),
                    Tempo(TempoType.Largo),
                    Tempo(TempoType.Vivace)
                    ]
        
        steps = [(Position(0), settings[0].tempo),
                 (Position(10), settings[1].tempo), 
                 (Position(20), settings[2].tempo),
                 (Position(30), settings[3].tempo),
                 (Position(40), settings[4].tempo)
                 ]
        f = StepwiseFunction(steps)
        event1 = TempoFunctionEvent(f, Position(10))
        
        t_hi_steady = Tempo(TempoType(TempoType.Vivace))
        event2 = TempoEvent(t_hi_steady, Position(50)) 
        
        tes = TempoEventSequence([event0, event1, event2]) 
        
        assert tes.tempo(Position(0)) == t_lo_steady.tempo 
        assert tes.tempo(Position(5)) == t_lo_steady.tempo

        assert tes.tempo(Position(10)) == settings[0].tempo
        assert tes.tempo(Position(20)) == settings[1].tempo
        assert tes.tempo(Position(30)) == settings[2].tempo
        assert tes.tempo(Position(40)) == settings[3].tempo
        assert tes.tempo(Position(50)) == settings[4].tempo 
        assert tes.tempo(Position(60)) == t_hi_steady.tempo

    def test_book_tempo_sequence(self):
        print('----- test_book_tempo_sequence -----')

        seq = TempoEventSequence()
        seq.add(TempoEvent(Tempo(TempoType.Grave), Position(0)))
        seq.add(TempoEvent(Tempo(TempoType.Moderato), Position(10)))
        seq.add(TempoEvent(Tempo(TempoType.Vivace), Position(25)))
        seq.add(TempoEvent(Tempo(TempoType.Largo), Position(50)))

        event = seq.first
        while event is not None:
            print(event)
            event = seq.successor(event)

        print('----- End test_book_tempo_sequence -----')

        
if __name__ == "__main__":
    unittest.main()
