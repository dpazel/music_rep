"""

File: tempo_event_sequence.py

Purpose: An event sequence specialized to tempo events.

"""
from timemodel.event_sequence import EventSequence
from timemodel.tempo_function_event import TempoFunctionEvent


class TempoEventSequence(EventSequence):
    """
    An event sequence specialized to tempo events.
    """

    def __init__(self, event_list=None):
        """
        Constructor.

        Args:
            event_list: TempoEvents to initialize the sequence.
        """
        EventSequence.__init__(self, event_list)
        
    def tempo(self, position):
        tfe = self.floor_event(position)
        if isinstance(tfe, TempoFunctionEvent):
            next_tfe = self.successor(tfe)
            return tfe.tempo(position, next_tfe.time if next_tfe != None else None)
        else:
            return tfe.tempo()

        