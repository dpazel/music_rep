from misc.ordered_map import OrderedMap
from enum import Enum


# The following are global variables used by Dynamics, as we could not define these
# inside TempoType.
class DynamicsHelper:
    NAME_MAP = None
    DYNAMICS_VALUE_MAP = None
    DEFAULT_DYNAMICS = None
    DEFAULT_DYNAMICS_VELOCITY = None
    REVERSE_DYNAMICS_VELOCITY_MAP = None
    DYNAMICS_LIST = None


class Dynamics(Enum):
    """
    Class representing music dynamics.  We use PPPP through FFFF.
    Velocity values have been assigned based on 0-127 midi range.

    """
    PPPP = 1
    PPP = 2
    PP = 3
    P = 4
    MP = 5
    MF = 6
    F = 7
    FF = 8
    FFF = 9
    FFFF = 10

    def __str__(self):
        return self.name

    @staticmethod
    def class_init():
        if DynamicsHelper.NAME_MAP is not None:
            return
    
        DynamicsHelper.NAME_MAP = {
            Dynamics.PPPP:  'pianissississimo',
            Dynamics.PPP:   'pianississimo0',
            Dynamics.PP:    'pianissimo',
            Dynamics.P:     'piano',
            Dynamics.MP:    'mezzo piano',
            Dynamics.MF:    'messo forte',
            Dynamics.F:     'forte',
            Dynamics.FF:    'fortissimo',
            Dynamics.FFF:   'fortississimo',
            Dynamics.FFFF:  'fortissississimo',
        }
    
        DynamicsHelper.DYNAMICS_VALUE_MAP = {
            Dynamics.PPPP:  16,
            Dynamics.PPP:   24,
            Dynamics.PP:    33,
            Dynamics.P:     49,
            Dynamics.MP:    64,
            Dynamics.MF:    80,
            Dynamics.F:     96,
            Dynamics.FF:    112,
            Dynamics.FFF:   120,
            Dynamics.FFFF:  127,
        }

        DynamicsHelper.DYNAMICS_LIST = [
            Dynamics.PPPP,
            Dynamics.PPP,
            Dynamics.PP,
            Dynamics.P,
            Dynamics.MP,
            Dynamics.MF,
            Dynamics.F,
            Dynamics.FF,
            Dynamics.FFF,
            Dynamics.FFFF,
        ]
    
        DynamicsHelper.DEFAULT_DYNAMICS = Dynamics.MP
        DynamicsHelper.DEFAULT_DYNAMICS_VELOCITY = DynamicsHelper.DYNAMICS_VALUE_MAP[DynamicsHelper.DEFAULT_DYNAMICS]
        DynamicsHelper.REVERSE_DYNAMICS_VELOCITY_MAP = OrderedMap({value: key for (key, value) in
                                                                   DynamicsHelper.DYNAMICS_VALUE_MAP.items()})

    @property
    def velocity(self):
        return DynamicsHelper.DYNAMICS_VALUE_MAP[self]
    
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

    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return hash(self.name)   
    
    @staticmethod
    def get_types():
        return [DynamicsHelper.DYNAMICS_LIST]

    @staticmethod
    def DEFAULT_DYNAMICS_VELOCITY():
        return DynamicsHelper.DEFAULT_DYNAMICS_VELOCITY
    
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
            if dynamics < 1 or dynamics > len(DynamicsHelper.DYNAMICS_LIST):
                raise Exception('Out of range int for get_velocity_for {0}'.format(type(dynamics)))
            dynamics = DynamicsHelper.DYNAMICS_LIST[dynamics - 1]
        elif not isinstance(dynamics, Dynamics):
            raise Exception('Illegal argument type for get_velocity_for {0}'.format(type(dynamics)))
        return dynamics.velocity


# Initialize the static tables in the Dynamics class.
Dynamics.class_init()
