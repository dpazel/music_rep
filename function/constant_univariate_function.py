"""

File: constant_univariate_function.py

Purpose: Class defining a univarate function of constant value.

"""
from function.univariate_function import UnivariateFunction


class ConstantUnivariateFunction(UnivariateFunction):
    """
    Class defining a univarate function of constant value.
    """

    def __init__(self, value, domain_start, domain_end, restrict_domain=False):
        """
        Constructor.

        Args:
            value: the constant value
        domain_start: numeric-like that defines the start of a domain (first point)
        domain_end: numeric_like tat defines the end of a domain (last point)
        restrict_domain: boolean meaning to throw exception for evaluations outside the domain
        """
        self.value = value
        
        self.__domain_start = domain_start
        self.__domain_end = domain_end
        self.__restrict_domain = restrict_domain
        
    def eval(self, x):
        if self.restrict_domain:
            if x < self.domain_start or x > self.domain_end:
                raise Exception('out of range {0} [{1}, {2}]'.format(x, self.domain_start, self.domain_end))
        return self.value
    
    @property
    def domain_start(self):
        return self.__domain_start
        
    @property
    def domain_end(self):
        return self.__domain_end
    
    @property
    def restrict_domain(self):
        return self.__restrict_domain
    
    def __str__(self):
        return 'Function(cst, {0})'.format(self.value)
