"""

File: tempo_event.py

Purpose: Defines a tempo as an Event  

"""
from timemodel.event import Event


class TempoEvent(Event):
    """
    Defines tempo as an Event, given a Tempo and a time position.
    """

    def __init__(self, tempo, time):
        """
        Constructor.
        
        Args:
          tempo:(Tempo) object.
          time: Comparable object.
        """
        Event.__init__(self, tempo, time)
        
    def tempo(self, position):
        return self.object.tempo
    
    def __str__(self):
        return '[{0}, Tempo({1})]'.format(self.time, self.object)
