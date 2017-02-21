"""

File: dynamics_function_event.py

Purpose: An event subclass (type) that defines the event in terms of dynamics or a functional dynamic. 

"""
from timemodel.event import Event
from structure.dynamics_function import DynamicsFunction
from timemodel.offset import Offset
from timemodel.offset import Duration


class DynamicsFunctionEvent(Event):
    """
    Event class for events that represent a dynamics or a dynamics function.
    """

    def __init__(self, dynamics_or_function, time):
        """
        Constructor
        
        Args:
          dynamics_or_function: Either a Dynamics setting or a Function
        """
        objct = DynamicsFunction(dynamics_or_function)
        Event.__init__(self, objct, time)
        
    def velocity(self, position, next_event_position):
        """
        Compute the velocity at a given position (re: DynamicsEventSequence)
        
        Args:
          position: The absolute position (Position) to evaluate at
          next_event_position:  The position (Position) of the starting of the next event.  Can be None is none exists.
        Returns:
          velocity as numerics [0-127] typically
        """
        return self.object.velocity(Offset(position.position - self.time.position),
                                    next_event_position - self.time if next_event_position else Duration(1))
    
    def dynamics(self, position, next_event_position):
        """
        Compute the velocity at a given position (re:DynamicsEventSequence.
        
        Args:
          position: The absolute position (Position) to evaluate at
          next_event_position:  The position (Position) of the starting of the next event.  Can be None is none exists,
          function range is used.
        Returns:
          velocity as Dynamics position
        """
        return self.object.dynamics(
            position - self.time, next_event_position - self.time if next_event_position else
            self.objct.function_range())
