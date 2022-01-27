"""

File: time_signature_event.py

Purpose: Defines a time signature as an Event. 

"""
from timemodel.event import Event
from timemodel.position import Position


class TimeSignatureEvent(Event):
    """
    Defines a time signature as an Event.
    """

    def __init__(self, time_signature, time):
        """
        Constructor.
        
        Args:
          time_signature: (TimeSignature) object.
          time: Position.
        """
        if not isinstance(time, Position):
           raise Exception('time argument to TimeSignatureEvent must be Position not \'{0}\'.'.format(type(time)))
        Event.__init__(self, time_signature, time)

    def time_signature(self):
        return self.object.time_signature

    def __str__(self):
        return '[{0}, TimeSignature({1})]'.format(self.time, self.object)