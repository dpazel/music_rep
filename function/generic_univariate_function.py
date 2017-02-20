"""

File: generic_univariate_function.py

Purpose: Allows a user defined function to be wrapped into the univariate framework.

"""
from function.univariate_function import UnivariateFunction


class GenericUnivariateFunction(UnivariateFunction):
    """
    A generalization of UnivariateFunction that allows a user define function to be used.
    This is a wrapper for functions that are univariate but not necessarily a subclass of UnivariateFunction.
    """
    
    def __init__(self, f, domain_start, domain_end, restrict_domain=False):
        """
        Constructor.
        
        Args:
        f: Function user-defined that is univariate, but not necessarily a subclass of UnivariateFunction.
        domain_start: numeric-like that defines the start of a domain (first point)
        domain_end: numeric_like tat defines the end of a domain (last point)
        restrict_domain: boolean meaning to throw exception for evaluations outside the domain
        """
        self.__domain_start = domain_start
        self.__domain_end = domain_end
        
        self.__f = f
        
        self.__restrict_domain = restrict_domain
        
    @property
    def domain_start(self):
        return self.__domain_start
    
    @property
    def domain_end(self):
        return self.__domain_end
    
    @property
    def restrict_domain(self):
        return self.__restrict_domain
    
    @property
    def f(self):
        return self.__f
    
    def eval(self, x):
        if self.restrict_domain:
            if x < self.domain_start or x > self.domain_end:
                raise Exception('{0} must be in [{1}, {2}]'.format(x, self.domain_start, self.domain_end))
        return (self.f)(x)