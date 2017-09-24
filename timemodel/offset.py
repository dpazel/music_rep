"""

File: Offset.py

Purpose: Describes a general Offset type that can be independent of time.

"""

from fractions import Fraction
from timemodel.position import Position
from timemodel.duration import Duration


class Offset(object):
    """
    classdocs
    """

    def __init__(self, *args, **kwargs):
        # args -- tuple of anonymous arguments
        # kwargs -- dictionary of named arguments
        """
        Constructor
        
        Args (1 parameter only)
          [0] offset_fraction (Fraction)
          
        Args (2 parameters)
          [0] numerator (int)
          [1] denominator (int)
        """
        if len(args) == 1:
            if not isinstance(args[0], Fraction) and not isinstance(args[0], int) and not isinstance(args[0], float):
                raise Exception(
                    'Single argument to Duration must be fraction or int or float, not {0}.'.format(type(args[0])))
            offset_fraction = args[0] if isinstance(args[0], Fraction) else Fraction(args[0])
        elif len(args) == 2:
            if not isinstance(args[0], int) or not isinstance(args[1], int):
                raise Exception('For 2 arguments, both must be integer.')
            offset_fraction = Fraction(args[0], args[1])
        else:
            raise Exception('Only 1 or two arguments expected.')
            
        self.__offset = offset_fraction
     
    @property
    def offset(self):
        return self.__offset
    
    def __cmp__(self, other):
        return -1 if self.offset < other.offset else 1 if self.offset > other.offset else 0
    
    def __lt__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.offset < other
        return self.offset < other.offset
       
    def __le__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.offset <= other
        return self.offset <= other.offset
        
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.offset == other
        return self.offset == other.offset
    
    def __ne__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.offset != other
        return self.offset != other.offset
    
    def __gt__(self, other):
        if other is None:
            return False
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.offset > other
        return self.offset > other.offset

    def __ge__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int) or isinstance(other, float):
            return self.offset >= other
        return self.offset >= other.offset    
    
    def __add__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            return Offset(self.offset + other)
        elif isinstance(other, float):
            return Offset(self.offset + Fraction(other))
        elif isinstance(other, Duration):
            return Duration(self.offset + other.duration)
        elif isinstance(other, Position):
            return other + self
        elif isinstance(other, Offset):
            return Offset(self.offset + other.offset)
        else:
            raise Exception(
                '= operator for offset {0} cannot be applied to {1} of type {2}'.format(self, other, type(other)))
        
    def __radd__(self, other):
        return self + other
        
    def __iadd__(self, other):
        # We opt to make Offset so neutral that offset+=position or duration just augments offset
        # This turns out to be very useful, this overrides __add__ for position and duration arguments
        if isinstance(other, Position):
            other = Offset(other.position)
        elif isinstance(other, Duration):
            other = Offset(other.duration)
        return self + other
    
    def __sub__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            return Offset(self.offset - other)
        elif isinstance(other, float):
            return Offset(self.offset - Fraction(other))
        elif isinstance(other, Position):
            return Position(self.offset - other.position)
        elif isinstance(other, Duration):
            return Duration(self.offset - other.duration)
        elif isinstance(other, Offset):
            return Offset(self.offset - other.offset)
        else:
            raise Exception('- operator for offset {0} cannot can not subtract type {1}'.format(self, type(other)))
        
    def __rsub__(self, other):
        return -self.__sub__(other)
    
    def __isub__(self, other):
        # We opt to make Offset so neutral that offset-=position or duration just augments offset
        # This turns out to be very useful, this overrides __sub__ for position and duration arguments
        if isinstance(other, Position):
            other = Offset(other.position)
        elif isinstance(other, Duration):
            other = Offset(other.duration)
        return self - other
    
    def __neg__(self):
        return Offset(-self.offset)
    
    def __mul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            return Offset(self.offset * other)
        elif isinstance(other, float):
            return Offset(self.offset * Fraction(other))
        else:
            raise Exception('* operator for offset {0} cannot be used on type {1}'.format(self, type(other)))
        
    def __rmul__(self, other):
        return self * other
    
    def __imul__(self, other):
        return self.__mul__(other)   
    
    def __str__(self):
        return str(self.offset)
