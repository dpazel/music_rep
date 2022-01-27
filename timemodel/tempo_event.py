"""

File: tempo_event.py

Purpose: Defines a tempo as an Event  

"""
from timemodel.event import Event
from timemodel.position import Position


class TempoEvent(Event):
    """
    Defines tempo as an Event, given a Tempo and a time position.
    """

    def __init__(self, tempo, time):
        """
        Constructor.
        
        Args:
          tempo:(Tempo) object.
          time: Postion.
        """
        if not isinstance(time, Position):
           raise Exception('time argument to TempoEvent must be Position not \'{0}\'.'.format(type(time)))
        Event.__init__(self, tempo, time)

    def tempo(self):
        return self.object.tempo
    
    def __str__(self):
        return '[{0}, Tempo({1})]'.format(self.time, self.object)
