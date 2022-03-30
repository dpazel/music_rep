"""

File: time_signature_event_sequence.py

Purpose: Defines a list time signature events as an event sequence.

"""
from timemodel.event_sequence import EventSequence


class TimeSignatureEventSequence(EventSequence):
    """
    An event sequence specialized to tempo events.
    """

    def __init__(self, event_list=None):
        """
        Constructor.

        Args:
            event_list: list of TempoEvents to initialize the sequence.
        """
        EventSequence.__init__(self, event_list)

    def time_signature(self, position):
        tfe = self.floor_event(position)
        return tfe.tempo()
