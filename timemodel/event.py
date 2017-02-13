"""

File: event.py

Purpose: Defines the Event class, being member to event_sequence.  

"""


class Event(object):
    """
    Defines the Event class, being member to event_sequence. 
    """

    def __init__(self, objct, time):
        """
        Constructor.
        
        Args:
          objct:  Any object
          time:  An comparable usually representing time, i.e. must define __eq__ and __lt__.
        """
        self.__object = objct
        self.__time = time
        
        if not time:
            raise Exception('Attempt to define and event without a time element')
        
    @property
    def object(self):
        return self.__object
    
    @object.setter
    def object(self, new_object):
        self.__object = new_object
    
    @property
    def time(self):
        """
        Should not be exposed to the user, and must me used with care, e.g. if part of an event sequence,
        the sequence time should be coordinated.
        """
        return self.__time
    
    @time.setter
    def time(self, new_time):
        self.__time = new_time
    
    def __str__(self):
        return '[{0}, {1}]'.format(self.time, self.object)
