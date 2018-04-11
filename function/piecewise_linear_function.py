"""

File: piecewise_linear_function.py

Purpose: Defines a piecewise linear function based on a set of transition points that define the steps.

"""
from function.univariate_function import UnivariateFunction
from misc.ordered_map import OrderedMap
from misc.utility import convert_to_numeric


class LinearSegment(object):
    """
    This class defines a linear segement based on two tuples of coordinates.
    """
    def __init__(self, start_coords, end_coords):
        """
        A linear segement between two sets of coordinates.
        :param start_coords: (x, y) of the first coordinate.
        :param end_coords: (x, y) of the second coordinte.
        """
        self.domain_start = start_coords[0]
        self.domain_end = end_coords[0]

        self.xcoef = (end_coords[1] -
                      start_coords[1])/float((convert_to_numeric(self.domain_end) -
                                              convert_to_numeric(self.domain_start)))
        self.ycoef = start_coords[1] - self.xcoef * convert_to_numeric(self.domain_start)
        
    def eval(self, value):
        return self.xcoef * value + self.ycoef


class PiecewiseLinearFunction(UnivariateFunction):
    """
    Piecewise linear function, steps defined by a set of transition points, where values between the ordinates
    of adjacent transitions points, are based on a linear interpolation of the transition points' values.
    
    For example, (3, 5), (7, 10), (10, 14), (12, 2)  has the following steps:
       (-3, 5
       (3-7, 5),
       (7-10, 10),
       (10-12, 14),
       (12-, 2)
       
       if restrict_domain is specified (True), evaluation points must be within domain bounds.
    """

    def __init__(self, transition_points=list(), restrict_domain=False):
        """
        Constructor.
        
        Args:
        transition_points: non-empty list of ordered pairs (x, y), x is the domain, y the range.
        restrict_domain: boolean indicating if evaluation points must be in defined domain of transition points.
                         default is False.
        """
        if transition_points is None or not isinstance(transition_points, list):
            assert Exception('Illegal argument to SetwiseLinearFunction {0}'.format(transition_points))
        self.__restrict_domain = restrict_domain
        self._setup(transition_points)
        
    def _setup(self, transition_points):
        self.__transition_points = sorted(transition_points, key=lambda x: x[0])
        self.__domain_start = self.__transition_points[0][0]
        self.__domain_end = self.__transition_points[len(self.__transition_points) - 1][0]
        
        lin_segs = []
        for i in range(0, len(self.transition_points) - 1):
            lin_segs.append((self.transition_points[i][0],
                             LinearSegment(self.transition_points[i], self.transition_points[i + 1])))
        
        self.ordered_map = OrderedMap(lin_segs)
        
    @property
    def transition_points(self):
        return self.__transition_points
    
    @property
    def restrict_domain(self):
        return self.__restrict_domain
    
    @property
    def domain_start(self):
        return self.__domain_start
    
    @property
    def domain_end(self):
        return self.__domain_end

    def __call__(self, x):
        return self.eval(x)
        
    def eval(self, x):
        if len(self.transition_points) == 0:
            raise Exception("The function is undefined due to lack of transition points.")
        if self.restrict_domain:
            if x < self.domain_start or x > self.domain_end:
                raise Exception('Input {0} out of range [{1}, {2}]'.format(x, self.domain_start, self.domain_end))

        if x <= self.domain_start:
            return self.transition_points[0][1]
        if x >= self.domain_end:
            return self.transition_points[len(self.transition_points) - 1][1]
        key = self.ordered_map.floor(x)
        lin_seg = self.ordered_map.get(key)
        return lin_seg.eval(x)
    
    def add(self, transition_point):
        """
        Add a transition point to the piecewise function.
        
        Args:
          transition_point: Pair (x, y)  x, y are numerics.
        """
        new_points = list(self.transition_points)
        new_points.append(transition_point)
        self._setup(new_points)
        
    def add_and_clear_forward(self, transition_point):
        """
        Add a transition point to the piecewise function AND clear out higher (domain value) transition points.
        
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
