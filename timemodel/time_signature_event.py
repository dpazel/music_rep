"""

File: time_signature_event.py

Purpose: Defines a time signature as an Event. 

"""
from timemodel.event import Event


class TimeSignatureEvent(Event):
    """
    Defines a time signature as an Event.
    """

    def __init__(self, time_signature, time):
        """
        Constructor.
        
        Args:
          time_signature: (TimeSignature) object.
          time: Comparable object.
        """
        Event.__init__(self, time_signature, time)