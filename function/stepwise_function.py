"""
File: stepwise_function.py

Purpose: Defines a stepwise linear function based on a set of transition points that define the steps.

"""
from function.univariate_function import UnivariateFunction
from misc.ordered_map import OrderedMap


class StepwiseFunction(UnivariateFunction):
    """
    Stepwise function, steps defined by a set of transition points
    
    For example, (5, 1), (7, 3), (10, 6), (12, 8)  has the following linear segments:
    (5, 1) to (7, 3)
    (7, 3) to (10, 6)
    (10, 6) to 12, 8)
             
    if restrict_domain is specified (True), evaluation points must be within domain bounds.
    """

    def __init__(self, transition_points=None, restrict_domain=False):
        """
        Constructor.
        
        Args:
        transition_points: non-empty list of ordered pairs (x, y)
        restrict_domain: boolean indicating if evaluation points must be in defined domain of transition points.
                         default is False.
        """
        if transition_points is None:
            transition_points = list()
        if transition_points is None or not isinstance(transition_points, list):
            assert Exception('Illegal argument to SetwiseLinearFunction {0}'.format(transition_points))
        self.__restrict_domain = restrict_domain
        self._setup(transition_points)
        
    def _setup(self, transition_points):
        self.__transition_points = sorted(transition_points, key=lambda x: x[0])
        self.__domain_start = self.__transition_points[0][0]
        self.__domain_end = self.__transition_points[len(self.__transition_points) - 1][0]
        
        self.ordered_map = OrderedMap(self.transition_points)
        
    @property
    def transition_points(self):
        return self.__transition_points
    
    @property
    def domain_start(self):
        return self.__domain_start
    
    @property
    def domain_end(self):
        return self.__domain_end
    
    @property 
    def restrict_domain(self):
        return self.__restrict_domain
        
    def eval(self, x):
        if len(self.transition_points) == 0:
            raise Exception("The function is undefined due to lack of transition points.")
        if self.restrict_domain:
            if x < self.domain_start or x > self.domain_end:
                raise Exception('Input {0} out of range [{1}, {2}]'.format(x, self.domain_start, self.domain_end))
        key = self.ordered_map.floor(x)
        if key is None:
            return self.ordered_map.get(self.domain_start)
        if key == self.domain_end:
            return self.ordered_map.get(self.domain_end)
        else:
            return self.ordered_map.get(key)
        
    def add(self, transition_point):
        """
        Add a transition point to the stepwise function.
        
        Args:
          transition_point: Pair (x, y)  x, y are numerics.
        """
        new_points = list(self.transition_points)
        new_points.append(transition_point)
        self._setup(new_points)
        
    def add_and_clear_forward(self, transition_point):
        """
        Add a transition point to the stepwise function AND clear out higher (domain value) transition points.
        
        Args:
          transition_point: Pair (x, y)  x, y are numerics.
        """
        new_points = []
        elimination_value = transition_point[0]
    
        for p in self.transition_points:
            if p[0] < elimination_value:
                new_points.append(p) 
        new_points.append(transition_point)
    
        self._setup(new_points)
