"""

File: tempo_function_event.py

Purpose: An event subclass (type) that defines the event in terms of a dynamics function.  

"""
from timemodel.event import Event
from structure.tempo_function import TempoFunction
from timemodel.offset import Offset
from timemodel.duration import Duration
from function.univariate_function import UnivariateFunction
from structure.tempo import Tempo


class TempoFunctionEvent(Event):
    """
    An event subclass (type) that defines the event in terms of a dynamics function.  
    """

    def __init__(self, tempo_function, time, beat_duration=None):
        """
        Constructor.
        
        Args:
            tempo_function: TempoFunction behind this event.
            beat_duration: Duration for the beat.
        """
        if not isinstance(tempo_function, UnivariateFunction) and not isinstance(tempo_function, Tempo):
            raise Exception('Input parameter must be UnivariateFunction or Tempo, not {0}'.format(type(tempo_function)))
        objct = TempoFunction(tempo_function, beat_duration)
        self.__beat_duration = beat_duration
        Event.__init__(self, objct, time)
        
    def tempo(self, position, next_event_position):
        """
        Compute the tempo at a given position (re: TempoEventSequence)
        
        Args:
          position: The absolute position (Position) to evaluate at
          next_event_position:  The position (Position) of the starting of the next event.  Can be None is none exists.
        Returns:
          tempo numeric as bpm based on tempo beat
        """
        return self.object.tempo(Offset(position.position - self.time.position),
                                 next_event_position - self.time if next_event_position else Duration(1))
        
    def beat_duration(self):
        return self.__beat_duration
