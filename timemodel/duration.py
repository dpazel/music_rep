"""

File: duration.py

Purpose: Defines duration as a class type.

"""

from fractions import Fraction

from timemodel.position import Position


class Duration(object):
    """
    Class to represent duration in music time.  This is primarily an encapsulation of Fraction,
    however, the typing is used to ensure some level of usage safety.  Ref. the operator overloading.
    """

    HALF = Fraction(1, 2)

    def __init__(self, *args, **kwargs):
        # args -- tuple of anonymous arguments
        # kwargs -- dictionary of named arguments
        """
        Constructor
        
        Args (1 parameter only)
          [0] duration_fraction (Fraction)
          
        Args (2 parameters)
          [0] numerator (int)
          [1] denominator (int)
        """
        if len(args) == 1:
            if isinstance(args[0], Duration):
                duration_fraction = args[0].duration
            elif not isinstance(args[0], Fraction) and not isinstance(args[0], int):
                raise Exception('Single argument to Duration must be fraction or int, not {0}.'.format(type(args[0])))
            else:
                duration_fraction = args[0] if isinstance(args[0], Fraction) else Fraction(args[0])
        elif len(args) == 2:
            if not isinstance(args[0], int) or not isinstance(args[1], int):
                raise Exception('For 2 arguments, both must be integer.')
            duration_fraction = Fraction(args[0], args[1])
        else:
            raise Exception('Only 1 or two arguments expected.')
            
        self.__duration = duration_fraction
        
    @property
    def duration(self):
        return self.__duration 
    
    @staticmethod
    def apply_half_dots(duration, num_dots):
        """
         Get the duration of a given duration with a number of dots applied.
         
         Args:
           duration: the duration to apply halving dots to
           num_dots: positive int value for number of dots
        Returns:
           new duration with number of dots applied to input duration.
        """
        target = Fraction(duration.duration.numerator, duration.duration.denominator)
        half_target = Fraction(duration.duration.numerator, duration.duration.denominator)
    
        while num_dots > 0:
            half_target *= Duration.HALF
            target = target + half_target
            num_dots -= 1
              
        return Duration(target)
    
    def apply_dots(self, num_dots):
        """
        Get the duration for this duration with number of dots applied.
        
        Args:
           num_dots: positive int value for number of dots to apply to self duration value
        Returns:
           new duration with number of dots applied to input duration.
        """
        return Duration.apply_half_dots(self, num_dots)
    
    def __cmp__(self, other):
        return -1 if self.duration < other.duration else 1 if self.duration > other.duration else 0
    
    def __lt__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.duration < other
        return self.duration < other.duration
       
    def __le__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.duration <= other
        return self.duration <= other.duration
        
    def __eq__(self, other):
        from timemodel.offset import Offset
        if other is None:
            return False
        elif isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.duration == other
        elif isinstance(other, Duration):
            return self.duration == other.duration
        elif isinstance(other, Offset):
            return self.duration == other.offset
        else:
            Exception('Cannot == compare Duration to type {0}.'.format(type(other)))
    
    def __ne__(self, other):
        from timemodel.offset import Offset
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.duration != other
        elif isinstance(other, Duration):
            return self.duration != other.duration
        elif isinstance(other, Offset):
            return self.duration != other.offset
        else:
            Exception('Cannot != compare Duration to type {0}.'.format(type(other)))
    
    def __gt__(self, other):
        if other is None:
            return False
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.duration > other
        if not isinstance(other, Duration):
            return False
        return self.duration > other.duration

    def __ge__(self, other):
        if other is None:
            return False
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.duration >= other
        if not isinstance(other, Duration):
            return False
        return self.duration >= other.duration
        
    def __add__(self, other):
        from timemodel.offset import Offset
        if isinstance(other, Fraction):
            return Duration(self.duration + other)
        if isinstance(other, int):
            return Duration(self.duration + other)
        elif isinstance(other, float):
            return Duration(self.duration + Fraction(other))
        elif isinstance(other, Duration):
            return Duration(self.duration + other.duration)
        elif isinstance(other, Position):
            return other + self
        elif isinstance(other, Offset):
            return Duration(self.duration + other.offset)
        else:
            raise Exception(
                '= operator for duration {0} cannot be applied to {1} of type {2}'.format(self, other, type(other)))
        
    def __radd__(self, other):
        return self + other
        
    def __iadd__(self, other):
        # dur = dur + position not possible, it is pos = pos + duration
        if isinstance(other, Position):
            raise Exception('+= operator for duration {0} cannot be applied to position {1}'.format(self, other))
        return self + other
    
    def __sub__(self, other):
        from timemodel.offset import Offset
        if isinstance(other, Fraction) or isinstance(other, int):
            return Duration(self.duration - other)
        if isinstance(other, float):
            return Duration(self.duration - Fraction(other))
        elif isinstance(other, Duration):
            return Duration(self.duration - other.duration)
        elif isinstance(other, Position):
            return Position(self.duration - other.position)
        elif isinstance(other, Offset):
            return Duration(self.duration - other.offset)
        else:
            raise Exception('- operator for duration {0} cannot can not subtract type {1}'.format(self, type(other)))
        
    def __rsub__(self, other):
        return -self.__sub__(other)
    
    def __isub__(self, other):
        if isinstance(other, Position):
            raise Exception('-= operator for duration {0} cannot be applied to position {1}'.format(self, other))
        return self - other
    
    def __neg__(self):
        return Duration(-self.duration)
    
    def __mul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            return Duration(self.duration * other)
        elif isinstance(other, float):
            return Duration(self.duration * Fraction(other))
        else:
            raise Exception('* operator for duration {0} cannot be used on type {1}'.format(self, type(other)))
        
    def __rmul__(self, other):
        return self * other
    
    def __imul__(self, other):
        return self.__mul__(other)

    def __hash__(self):
        return hash(str(self))
    
    def __str__(self):
        return str(self.duration)
