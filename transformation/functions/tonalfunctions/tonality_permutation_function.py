"""

File: tonality_permutation_function.py

Purpose: Class defining a function based on a permutation of a tonality's tones.

"""
from transformation.functions.tonalfunctions.tonal_function import TonalFunction
from transformation.functions.tonalfunctions.tonality_permutation import TonalityPermutation


class TonalityPermutationFunction(TonalFunction):
    """
    Class implementation of a function based on a tonality permutation.
    """

    def __init__(self, tonality_permutation, extension_map=None):
        """
        Concstructor using a tonality permutation.
        :param domain_tonality:
        :param tonality_permutation: TonalityPermutation.
        :param extension_map:

        Note: the permutation_cycles is strictly used for initialization. During usage, settings and deletes may
        change the mapping of the given tonality's tones.
        """
        self._tonality_permutation = tonality_permutation
        domain_tonality = tonality_permutation.tonality
        primary_map = tonality_permutation.map

        TonalFunction.__init__(self, domain_tonality, domain_tonality, primary_map, extension_map)

    @staticmethod
    def create(tonality, cycles, extension_map = None):
        """
        Construction using a tonality and cycles.
        :param tonality:
        :param cycles:
        :param extension_map:
        :return:
        """
        return TonalityPermutationFunction(TonalityPermutation(tonality, cycles), extension_map)

    @property
    def tonality_permutation(self):
        return self._tonality_permutation

    def __str__(self):
        return str(self.tonality_permutation)
