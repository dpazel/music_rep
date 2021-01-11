"""

File: generic_univariate_pitch_function.py

Purpose: Class providing means to define a univariate function that acts as a pitch function.

"""
from function.function_pitch_range import FunctionPitchRange
from function.generic_univariate_function import GenericUnivariateFunction


class GenericUnivariatePitchFunction(GenericUnivariateFunction, FunctionPitchRange):
    """
    GenericUnivariatePitchFunction - Does 2 things:
       1) Builds a univariate function using a using supplied function
       2) Provides methods from FunctionPitchRange to evaluate to pitches, chromatic distances, and frequencies.
    """

    def __init__(self, f, domain_start, domain_end, restrict_domain=False, interp=None):
        """
        Constructor
        :param f: User supplied function that evaluates to a value meaningful to a PitchRangeInterpreter.
        :param domain_start: numeric value for start of domain.
        :param domain_end: numeric value for end of domain.
        :param restrict_domain: True means adhere strictly to domain specification.
        :param interp: A PitchRangeInterpreter that maps f range values to pitches.  If None, ChromaticRangeInterpreter
                       is used.
        """

        # This instance is a GenericUnivariateFunction that evaluates f to a value in chromatic range
        GenericUnivariateFunction.__init__(self, f, domain_start, domain_end, restrict_domain)
        # This instance is also a FunctionPitchRange that maps the range of f to a pitch
        FunctionPitchRange.__init__(self, self, interp)