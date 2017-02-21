"""
Created on Sep 15, 2016
File: dynamics_function.py

Purpose: A function wrapper for Dynamics.  For a Dynamics, builds a constant function, otherwise uses a given function. 

@author: donald p pazel
"""
from structure.dynamics import Dynamics
from function.constant_univariate_function import ConstantUnivariateFunction
from misc.utility import convert_to_numeric
from numbers import Rational
from function.univariate_function import UnivariateFunction


class DynamicsFunction(object):
    """
    A functional wrapper for Dynamics. Constructs a constant function for a given Dynamics setting, or Rational setting,
        otherwise uses the given function for evaluation.
    """

    def __init__(self, dynamics_or_function):
        """
        Constructor
        
        Args: (Dynamics, Rational, or Function)
        """
        if isinstance(dynamics_or_function, Dynamics):
            self.fctn = ConstantUnivariateFunction(dynamics_or_function.velocity, 0, 1)
        elif isinstance(dynamics_or_function, Rational):
            self.fctn = ConstantUnivariateFunction(dynamics_or_function, 0, 1)
        elif isinstance(dynamics_or_function, UnivariateFunction):
            self.fctn = dynamics_or_function
        else:
            raise Exception('Illegal argument type {0)', type(dynamics_or_function))
                        
    def velocity(self, offset, duration):
        """
        Compute a velocity setting based on a given offset on domain defined by duration
        The offset is rescaled to the actual range of the function.
        
        Args:
          offset: (Offset) within duration
          duration: (Duration) of domain
        """
        # scale to functions domain
        q = (offset.offset/duration.duration) * (convert_to_numeric(self.fctn.domain_end) -
                                                 convert_to_numeric(self.fctn.domain_start))
        return self.fctn.eval(convert_to_numeric(self.fctn.domain_start) + q)
    
    def function_range(self):
        return self.fctn.domain_end - self.fctn.domain_start
    
    def dynamics(self, offset, duration):
        """
        Compute the velocity as a Dynamics setting.
        
         Args:
           offset: (Offset) within duration
           duration: (Duration) of domain
        """
        v = self.velocity(offset, duration)
        return Dynamics.nearest_dynamics(v)
    
    def __str__(self):
        return '[DyFctn({})]'.format(self.fctn)
