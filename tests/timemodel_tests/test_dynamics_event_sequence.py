import unittest
from timemodel.dynamics_event_sequence import DynamicsEventSequence
from timemodel.dynamics_function_event import DynamicsFunctionEvent
from structure.dynamics import Dynamics

from function.piecewise_linear_function import PiecewiseLinearFunction

from timemodel.position import Position
from function.stepwise_function import StepwiseFunction
from timemodel.dynamics_event import DynamicsEvent


class Test(unittest.TestCase):

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
        des = DynamicsEventSequence(events)
        
        assert des.velocity(Position(0)) == Dynamics.P
        assert des.velocity(Position(1, 4)) == Dynamics.P
        assert des.velocity(Position(1, 2)) == Dynamics.F
        assert des.velocity(Position(5, 8)) == Dynamics.F
        assert des.velocity(Position(3, 4)) == Dynamics.PP
        assert des.velocity(Position(1)) == Dynamics.FF
        assert des.velocity(Position(3, 2)) == Dynamics.FFF
        
        print des
        
    def test_crescendo_decrescendo_velocity(self):
        v_lo_steady = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.P] 
        event0 = DynamicsFunctionEvent(v_lo_steady, Position(0))
        
        v_low = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.P]
        v_hi = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.FF]
        array = [(Position(0), v_low),
                 (Position(1, 2), v_hi)]
        f = PiecewiseLinearFunction(array)
        event1 = DynamicsFunctionEvent(f, Position(1))
        
        v_hi_steady = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.FF]
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
        
        v_hi_steady = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.F] 
        event0 = DynamicsFunctionEvent(v_hi_steady, Position(0))
        
        v_hi = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.F]
        v_low = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.PP]
        array = [(Position(0), v_hi),
                 (Position(1, 3), v_low)]
        f = PiecewiseLinearFunction(array)
        event1 = DynamicsFunctionEvent(f, Position(1))
        
        v_lo_steady = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.PP]
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
        v_lo_steady = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.P]
        event0 = DynamicsEvent(Dynamics(Dynamics.P), Position(0))
        
        v_0 = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.P]
        v_1 = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.F]
        v_2 = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.FFF]
        v_3 = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.FF]
        steps = [(Position(1), v_0),
                 (Position(3, 2), v_1), 
                 (Position(7, 4), v_2),
                 (Position(2), v_3)
                 ]
        f = StepwiseFunction(steps)
        event1 = DynamicsFunctionEvent(f, Position(1))
        
        v_hi_steady = Dynamics.DYNAMICS_VALUE_MAP[Dynamics.FF]
        event2 = DynamicsFunctionEvent(v_hi_steady, Position(2))
        
        des = DynamicsEventSequence([event0, event1, event2]) 
        
        assert des.velocity(Position(0)) == v_lo_steady 
        assert des.velocity(Position(1, 2)) == v_lo_steady
        assert des.velocity(Position(3, 4)) == v_lo_steady
        assert des.velocity(Position(1)) == v_0
        assert des.velocity(Position(3, 2)) == v_1
        assert des.velocity(Position(7, 4)) == v_2
        assert des.velocity(Position(2)) == v_3


if __name__ == "__main__":
    unittest.main()
