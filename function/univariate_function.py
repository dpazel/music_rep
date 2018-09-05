"""

File: univariate_function.py

Purpose: Class that defines a generic (abstract) univariate function.

"""
from abc import ABC, abstractmethod


class UnivariateFunction(ABC):
    """
    Class that defines a generic (abstract) univariate function.
    """

    def __init(self):
        super().__init__()

    @abstractmethod
    def eval(self, v):
        """
        Evaluate the univariate function with input v, and return that value
        :param v: Typically some kind of numeric.
        :return:
        """
        pass
    
    @property
    @abstractmethod
    def domain_start(self):
        """
        Return the start value of the domain.
        :return:
        """
        pass

    @property
    @abstractmethod
    def domain_end(self):
        """
        Return the end value of the domain.
        :return:
        """
        pass
