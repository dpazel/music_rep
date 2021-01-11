"""

File: tonal_permutation.py

Purpose: Class defining a function on one tonality based on a permatuation specification.

"""
from transformation.functions.tonalfunctions.tonal_permutation import TonalPermutation


class TonalityPermutation(TonalPermutation):
    """
    Class implementation of a permutation on a set of tones.
    More restrictive than Permutation, in that tones of a given tonality are the elements of the permutation.
    """

    def __init__(self, tonality, cycles=list()):
        """
        Constructor
        :param tonality:
        :param cycles:
        """
        self._tonality = tonality
        domain_tones = tonality.annotation[:len(tonality.annotation) - 1]
        TonalPermutation.__init__(self, cycles, domain_tones)

    @property
    def tonality(self):
        return self._tonality
