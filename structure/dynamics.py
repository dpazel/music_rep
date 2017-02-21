"""

File: dynamics.py

Purpose: Defines class for Dynamics

"""
from misc.ordered_map import OrderedMap


class Dynamics(object):
    """
    Class representing music dynamics.  We use PPPP through FFFF.
    Velocity values have been assigned based on 0-127 midi range.
    """
    PPPP, PPP, PP, P, MP, MF, F, FF, FFF, FFFF = range(10)
    
    NAME_MAP = {
            PPPP:  'pianissississimo',
            PPP:   'pianississimo0',
            PP:    'pianissimo',
            P:     'piano',
            MP:    'mezzo piano',
            MF:    'messo forte',
            F:     'forte',
            FF:    'fortissimo',
            FFF:   'fortississimo',
            FFFF:  'fortissississimo',
        }
    
    DYNAMICS_VALUE_MAP = {
            PPPP:  16,
            PPP:   24,
            PP:    33,
            P:     49,
            MP:    64,
            MF:    80,
            F:     96,
            FF:    112,
            FFF:   120,
            FFFF:  127,
        }
    
    DEFAULT_DYNAMICS = MP
    DEFAULT_DYNAMICS_VELOCITY = DYNAMICS_VALUE_MAP[DEFAULT_DYNAMICS]
    REVERSE_DYNAMICS_VELOCITY_MAP = OrderedMap({value: key for (key, value) in DYNAMICS_VALUE_MAP.items()})

    def __init__(self, type_value):
        """
        Constructor.
        
        Args:
          type_value: One of PPPP, ... FFFF
        """
        if type_value < Dynamics.PPPP or type_value > Dynamics.FFFF:
            raise Exception('Illegal value {0} for Dynamics'.format(type_value))
        self.__value = type_value 
        self.__name = Dynamics.NAME_MAP[self.__value]
        self.__velocity = Dynamics.DYNAMICS_VALUE_MAP[self.__value]
        
    @property
    def value(self):
        return self.__value
    
    @property
    def name(self):
        return self.__name
    
    @property
    def velocity(self):
        return self.__velocity
    
    @staticmethod
    def nearest_dynamics(value):
        """
        Return the nearest dynamics for a given velocity value.
        
        Args:
          value:  The velocity value.
        Returns: The nearest Dynamics as a Dynamics object.
        """
        if value <= Dynamics.DYNAMICS_VALUE_MAP[Dynamics.PPPP]:
            return Dynamics.PPPP
        if value >= Dynamics.DYNAMICS_VALUE_MAP[Dynamics.FFFF]:
            return Dynamics.FFFF
        d = Dynamics.REVERSE_DYNAMICS_VELOCITY_MAP.floor(value) 
        next_d = d.keys()[d.keys().index(d) + 1]
        return Dynamics(Dynamics.REVERSE_DYNAMICS_VELOCITY_MAP[d] if value <= (d + next_d)/2 else
                        Dynamics.REVERSE_DYNAMICS_VELOCITY_MAP[next_d])
               
    def __str__(self):
        return self.name
        
    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return hash(self.name)   
    
    @staticmethod
    def get_types():
        return [Dynamics(x) for x in range(Dynamics.PPPP, Dynamics.FFFF + 1)]
    
    @staticmethod
    def get_velocity_for(dynamics):
        """
        Static method to get the range for a tempo type.
        Args:
          dynamics: if integer, turned into Dynamics based on int.  Otherwise must be a Dynamics.
          
        Returns: velocity for type.
        Exception: on bad argument type.
        """
        if isinstance(dynamics, int):
            dynamics = Dynamics(dynamics)
        elif not isinstance(dynamics, Dynamics):
            raise Exception('Illegal argument type for get_velocity_for {0}'.format(type(dynamics)))
        return dynamics.velocity
