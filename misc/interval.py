"""

File: interval.py

Purpose: Interval class defines a numeric range object, and is primarily used in interval tree.

"""


class BoundaryPolicy:
    """
    Enum class that defines the boundary conditions on intervals, leaving 4 options:
        (a, b): Open
        [a, b]: Closed
        (a, b]: Low boundary open only
        [a, b): High boundary open only
    """
    Open, Closed, LO_Open, HI_Open = range(4)
    # Open,             (a, b)
    # Closed,           [a,b]
    # LO_OPEN,          (a, b]
    # HI_OPEN           [a, b)
    
    def __init__(self, itype):
        self.value = itype
        
    def __str__(self):
        if self.value == BoundaryPolicy.Open:
            return 'Open'
        if self.value == BoundaryPolicy.Closed:
            return 'Closed'
        if self.value == BoundaryPolicy.LO_Open:
            return 'LO_Open'
        if self.value == BoundaryPolicy.HI_Open:
            return 'HI_Open'
        
    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return self.__str__().__hash__()
  

class Interval(object):
    """
    Class defining an interval in the sense of real numbers defining a contiguous segment.
    """

    def __init__(self, lower, upper, policy=BoundaryPolicy.HI_Open):
        """
        Constructor.
        Args:
          lower: Rational or float, lower bound
          upper: Rational or float, upper bound
          policy: BoundaryPolicy defining endpoint constraints.
        """
        if lower > upper:
            raise Exception('Cannot specify Interval with lower > upper ({0} > {1})', lower, upper)
        
        self.__lower = lower
        self.__upper = upper
        self.__policy = policy
        
    @property
    def lower(self):
        return self.__lower
    
    @property
    def upper(self):
        return self.__upper
    
    @property
    def policy(self):
        return self.__policy

    def length(self):
        return self.upper - self.lower
    
    def contains(self, value):
        """
        Method to see of a rational value in contained in this interval.
        
        Args:
          value: Rational
        Returns: Boolean indicating if in boundary.
        """
        if self.policy == BoundaryPolicy.Open:
            return self.upper > value > self.lower
        if self.policy == BoundaryPolicy.Closed:
            return self.upper >= value >= self.lower
        if self.policy == BoundaryPolicy.LO_Open:
            return self.upper >= value > self.lower
        if self.policy == BoundaryPolicy.HI_Open:
            return self.upper > value >= self.lower
        
    @staticmethod
    def intersects(i1, i2):
        """
        Static methods that indicates if two intervals intersect
        
        Args:
          i1: Interval
          i2: Interval
        Returns: Boolean
        """
        return i1.contains(i2.lower) or i2.contains(i1.lower)
    
    def intersection(self, interval):
        """
        Method to return the intersection (Interval) of self and a given interval.
        
        Args:
          interval: Interval
        Returns:
          Interval intersection of self and interval, or None if they do not intersect.
        """
        if not Interval.intersects(self, interval):
            return None
    
        lo = interval.lower if self.contains(interval.lower) else self.lower
        lo_policy = interval.policy if self.contains(interval.lower) else self.policy
    
        hi = interval.upper if self.contains(interval.upper) else self.upper
        hi_policy = interval.policy if self.contains(interval.upper) else self.policy

        if lo_policy == hi_policy:
            bp = lo_policy
        else:
            if lo_policy == BoundaryPolicy.Open or lo_policy == BoundaryPolicy.LO_Open:
                bp = BoundaryPolicy.LO_Open
            else:
                bp = BoundaryPolicy.HI_Open
    
        return Interval(lo, hi, bp)
    
    @staticmethod
    def intersect(i1, i2):
        """
        Method to compute intersection of two Intervals.
        
        Args:
          i1: Interval
          i2: Interval
        Returns: 
          Interval intersection of i1 and i2.
        """
        return i1.intersection(i2)
    
    def __eq__(self, other):
        if not other:
            return False
        if isinstance(other, self.__class__):
            return self.lower == other.lower and self.upper == other.upper and self.policy == other.policy
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
  
    def __str__(self):
        if self.policy == BoundaryPolicy.Open:
            return '({0}, {1})'.format(self.lower, self.upper)
        if self.policy == BoundaryPolicy.Closed:
            return '[{0}, {1}]'.format(self.lower, self.upper)
        if self.policy == BoundaryPolicy.LO_Open:
            return '({0}, {1}]'.format(self.lower, self.upper)
        if self.policy == BoundaryPolicy.HI_Open:
            return '[{0}, {1})'.format(self.lower, self.upper)
