"""

File: univariate_function.py

Purpose: Class that defines a generic (abstract) univariate function.

"""

from abc import ABCMeta, abstractmethod, abstractproperty

class UnivariateFunction(object):
    """
    Class that defines a generic (abstract) univariate function.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def eval(self, v):
        pass
    
    @abstractproperty
    def domain_start(self):
        pass
        
    @abstractproperty
    def domain_end(self):
        pass
        