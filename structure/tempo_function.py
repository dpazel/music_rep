"""

File: tempo_function.py

Purpose: A function wrapper for Tempo.  For a Tempo, builds a constant function, otherwise uses a given function. 

"""
from numbers import Rational

from structure.tempo import Tempo
from function.constant_univariate_function import ConstantUnivariateFunction
from function.univariate_function import UnivariateFunction
from timemodel.duration import Duration
from misc.utility import convert_to_numeric


class TempoFunction(object):
    """
    A functional wrapper for Tempo. Constructs a constant function for a given Tempo setting, or Rational setting,
        otherwise uses the given function for evaluation.
    """

    def __init__(self, tempo_or_function, beat_duration=None):
        """
        Constructor
        .
        Args:
            tempo_or_function: Tempo for constant, Rational for constant, or UnivariateFunction.
            beat_duration: whole note time duration (Duration) for a beat.
        """
        if isinstance(tempo_or_function, Tempo):
            self.fctn = ConstantUnivariateFunction(tempo_or_function.tempo, 0, 1)
            if beat_duration:
                raise Exception('Cannot specify beat_duration with Tempo specified.')
            self.beat_duration = tempo_or_function.beat_duration
        elif isinstance(tempo_or_function, Rational):
            self.fctn = ConstantUnivariateFunction(tempo_or_function, 0, 1)
            if not beat_duration:
                beat_duration = Duration(1, 4)
            self.beat_duration = beat_duration
        elif isinstance(tempo_or_function, UnivariateFunction):
            self.fctn = tempo_or_function
            if not beat_duration:
                beat_duration = Duration(1, 4)
            self.beat_duration = beat_duration
        else:
            raise Exception('Illegal argument type {0)', type(tempo_or_function))
        
    def tempo(self, offset, duration):
        """
        Compute a tempo (bpm) setting based on a given offset on domain defined by duration
        The offset is rescaled to the actual range of the function.
        
        Args:
          offset: (Offset) within duration
          duration: (Duration) of domain
        Returns:
          bpm value based on tempo information provided by self.fctn
        """
        # scale to functions domain
        q = (offset.offset/duration.duration) * (convert_to_numeric(self.fctn.domain_end) -
                                                 convert_to_numeric(self.fctn.domain_start))
        return self.fctn.eval(convert_to_numeric(self.fctn.domain_start) + q)

    def __str__(self):
        return '[TempoFctn({0}) per {1} note]'.format(self.fctn, self.beat_duration)
