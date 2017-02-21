"""

File: dynamics_event_sequence.py

Purpose: Specialization of event sequence for dynamics.
"""
from timemodel.event_sequence import EventSequence
from timemodel.dynamics_function_event import DynamicsFunctionEvent

class DynamicsEventSequence(EventSequence):
    '''
    Specialization of event sequence for dynamics.
    '''

    def __init__(self, event_list = None):
        """
        Constructor.

        Args:
            event_list: list of events to initialize the sequence
        """
        EventSequence.__init__(self, event_list)
        
    def velocity(self, position):
        dfe = self.floor_event(position)
        if isinstance(dfe, DynamicsFunctionEvent):
            next_dfe = self.successor(dfe)
            return dfe.velocity(position, next_dfe.time if next_dfe != None else None)
        else:
            return dfe.velocity()

        