"""

File: function_pitch_range.py

Purpose: Takes a univarate function as a means to map to pitch range.

"""
import math

from function.chromatic_range_interpreter import ChromaticRangeInterpreter
from tonalmodel.chromatic_scale import ChromaticScale


class FunctionPitchRange(object):
    """
    FunctionPitchRange - Used as a base class to build functions that map to pitch ranges.
      Provides the following:
      1) Map to chromatic distance (1/2 steps) as float.
      2) Map to frequencey
      3) Map to log frequency
      4) Map to the nearest pitch in the diatonic scale (see DiatonicFoundation).
      5) Map to nearest lower and upper pitches.
    """

    def __init__(self, univariate_function, pitch_range_interpreter=ChromaticRangeInterpreter()):
        """
        Constructor.
        :param univariate_function: Univariate Function
        """
        self.__univariate_function = univariate_function
        self.__pitch_range_interpreter = pitch_range_interpreter if pitch_range_interpreter is not None \
            else ChromaticRangeInterpreter()

    @property
    def univariate_function(self):
        return self.__univariate_function

    @property
    def pitch_range_interpreter(self):
        return self.__pitch_range_interpreter

    # should be renamed, this is f(v) where f is the univariate function.
    def eval_as_chromatic_distance(self, v):
        return self.univariate_function.eval(v)

    def eval_as_frequency(self, v):
        cd = self.eval_as_chromatic_distance(v)

        exponent = cd - ChromaticScale.CHROMATIC_START[1]
        return ChromaticScale.A0 * pow(ChromaticScale.SEMITONE_RATIO, exponent)

    def eval_as_log_frequency(self, v):
        return math.log10(self.eval_as_frequency(v))

    def eval_as_nearest_pitch(self, v):
        return self.pitch_range_interpreter.eval_as_nearest_pitch(self.eval_as_chromatic_distance(v))

    def eval_as_pitch(self, v):
        return self.pitch_range_interpreter.eval_as_pitch(self.eval_as_chromatic_distance(v))

    def eval_as_accurate_chromatic_distance(self, v):
        return self.pitch_range_interpreter.eval_as_accurate_chromatic_distance(self.eval_as_chromatic_distance(v))



