import unittest
from timemodel.dynamics_event_sequence import DynamicsEventSequence
from timemodel.dynamics_function_event import DynamicsFunctionEvent
from structure.dynamics import Dynamics

from function.piecewise_linear_function import PiecewiseLinearFunction

from timemodel.position import Position
from function.stepwise_function import StepwiseFunction
from timemodel.dynamics_event import DynamicsEvent


class TestDynamicsEventSequence(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_sequence(self):
        events = [DynamicsFunctionEvent(Dynamics.P, Position(0)), 
                  DynamicsFunctionEvent(Dynamics.F, Position(1, 2)), 
                  DynamicsFunctionEvent(Dynamics.PP, Position(3, 4)), 
                  DynamicsFunctionEvent(Dynamics.FF, Position(1)), 
                  DynamicsFunctionEvent(Dynamics.FFF, Position(3, 2)) 
                  ]
        seq = DynamicsEventSequence(events)
        
        assert seq.velocity(Position(0)) == Dynamics.P.velocity
        assert seq.velocity(Position(1, 4)) == Dynamics.P.velocity
        assert seq.velocity(Position(1, 2)) == Dynamics.F.velocity
        assert seq.velocity(Position(5, 8)) == Dynamics.F.velocity
        assert seq.velocity(Position(3, 4)) == Dynamics.PP.velocity
        assert seq.velocity(Position(1)) == Dynamics.FF.velocity
        assert seq.velocity(Position(3, 2)) == Dynamics.FFF.velocity
        
        print(seq)
        
    def test_crescendo_decrescendo_velocity(self):
        v_lo_steady = Dynamics.P.velocity
        event0 = DynamicsFunctionEvent(v_lo_steady, Position(0))
        
        v_low = Dynamics.P.velocity
        v_hi = Dynamics.FF.velocity
        array = [(Position(0), v_low),
                 (Position(1, 2), v_hi)]
        f = PiecewiseLinearFunction(array)
        event1 = DynamicsFunctionEvent(f, Position(1))
        
        v_hi_steady = Dynamics.FF.velocity
        event2 = DynamicsFunctionEvent(v_hi_steady, Position(2))

        des = DynamicsEventSequence([event0, event1, event2])
        
        assert des.velocity(Position(0)) == v_lo_steady
        assert des.velocity(Position(1, 2)) == v_lo_steady
        assert des.velocity(Position(3, 4)) == v_lo_steady
        assert des.velocity(Position(1)) == v_lo_steady
        assert des.velocity(Position(3, 2)) == (v_low + v_hi) / 2.0
        assert des.velocity(Position(7, 4)) == v_low + 3 * (v_hi - v_low) / 4.0
        assert des.velocity(Position(2)) == v_hi
        assert des.velocity(Position(3)) == v_hi_steady
        
        v_hi_steady = Dynamics.F.velocity
        event0 = DynamicsFunctionEvent(v_hi_steady, Position(0))
        
        v_hi = Dynamics.F.velocity
        v_low = Dynamics.PP.velocity
        array = [(Position(0), v_hi),
                 (Position(1, 3), v_low)]
        f = PiecewiseLinearFunction(array)
        event1 = DynamicsFunctionEvent(f, Position(1))
        
        v_lo_steady = Dynamics.PP.velocity
        event2 = DynamicsFunctionEvent(v_lo_steady, Position(2))
                
        des = DynamicsEventSequence([event0, event1, event2])
        
        assert des.velocity(Position(0)) == v_hi_steady
        assert des.velocity(Position(1, 2)) == v_hi_steady
        assert des.velocity(Position(3, 4)) == v_hi_steady
        assert des.velocity(Position(1)) == v_hi_steady
        
        assert des.velocity(Position(3, 2)) == (v_low + v_hi) / 2.0
        assert des.velocity(Position(7, 4)) == v_hi - 3 * (v_hi - v_low) / 4.0
        assert des.velocity(Position(2)) == v_low
        assert des.velocity(Position(3)) == v_lo_steady
        
    def test_step_wise_velocity(self):
        v_lo_steady = Dynamics.P.velocity
        event0 = DynamicsEvent(Dynamics.P, Position(0))
        
        v_0 = Dynamics.P.velocity
        v_1 = Dynamics.F.velocity
        v_2 = Dynamics.FFF.velocity
        v_3 = Dynamics.FF.velocity
        steps = [(Position(1), v_0),
                 (Position(3, 2), v_1), 
                 (Position(7, 4), v_2),
                 (Position(2), v_3)
                 ]
        f = StepwiseFunction(steps)
        event1 = DynamicsFunctionEvent(f, Position(1))
        
        v_hi_steady = Dynamics.FF.velocity
        event2 = DynamicsFunctionEvent(v_hi_steady, Position(2))
        
        des = DynamicsEventSequence([event0, event1, event2]) 
        
        assert des.velocity(Position(0)) == v_lo_steady 
        assert des.velocity(Position(1, 2)) == v_lo_steady
        assert des.velocity(Position(3, 4)) == v_lo_steady
        assert des.velocity(Position(1)) == v_0
        assert des.velocity(Position(3, 2)) == v_1
        assert des.velocity(Position(7, 4)) == v_2
        assert des.velocity(Position(2)) == v_3
