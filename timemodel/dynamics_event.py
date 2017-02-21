"""

File: tempo.py

Purpose: Defines a dynamics as an Event 

"""
from timemodel.event import Event
from structure.dynamics import Dynamics

class DynamicsEvent(Event):
    """
    Event based on Dynamics
    """

    def __init__(self, dynamics, time):
        """
        Constructor.
        
        Args:
          dynamics: (Dynamics) object.
          time: Comparable object.
        """
        Event.__init__(self, dynamics, time)
        
        if dynamics is None or not isinstance(dynamics, Dynamics):
            raise Exception('Dynamics event argument must be not null and Dynamics')
        
    def velocity(self):
        return self.object.velocity
    
    def __str__(self):
        return '[{0}, Dynamics({1})]'.format(self.time, self.object)
    
    def dynamics(self):
        return self.object
