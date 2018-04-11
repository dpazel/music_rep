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
        pass
    
    @property
    @abstractmethod
    def domain_start(self):
        pass

    @property
    @abstractmethod
    def domain_end(self):
        pass
