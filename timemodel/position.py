"""
File: position.py

Purpose: Defines position as a class type.

"""
from fractions import Fraction


class Position(object):
    """
    Class to represent position in music time.  This is primarily an encapsulation of Fraction,
    however, the typing is used to ensure some level of usage safety.  Ref. the operator overloading.
    """

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
        from timemodel.duration import Duration
        if len(args) == 1:
            if isinstance(args[0], int):
                position_fraction = Fraction(args[0], 1)
            elif isinstance(args[0], Position):
                position_fraction = args[0].position
            elif isinstance(args[0], Duration):
                position_fraction = args[0].duration
            elif not isinstance(args[0], Fraction):
                raise Exception('Cannot create Position with {0} as type {1}', args[0], type(args[0]))
            else:
                position_fraction = args[0]
        elif len(args) == 2:
            if not isinstance(args[0], int) or not isinstance(args[1], int):
                raise Exception('Cannot create Position with {0}, {1] wity types {2}, {3}', args[0], args[1],
                                type(args[0]), type(args[1]))
            position_fraction = Fraction(args[0], args[1])
        else:
            raise Exception('Cannot create Position with {0} arguments', len(args))
            
        self.__position = position_fraction
        
    @property
    def position(self):
        return self.__position
    
    def __cmp__(self, other):
        return -1 if self.position < other.position else 1 if self.position > other.position else 0
    
    def __lt__(self, other):
        if isinstance(other, Position):
            return self.position < other.position
        else:
            return self.position < other
       
    def __le__(self, other):
        if isinstance(other, Position):
            return self.position <= other.position
        else:
            return self.position <= other
        
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Position):
            return self.position == other.position
        elif isinstance(other, int) or isinstance(other, float) or isinstance(other, Fraction):
            return self.position == other
        else:
            return Exception('Cannot == compare Position to type {0}.'.format(type(other)))
        
    def __hash__(self):
        return hash(self.position)
    
    def __ne__(self, other):
        if other is None:
            return False
        if isinstance(other, Position):
            return self.position != other.position
        elif isinstance(other, int) or isinstance(other, float) or isinstance(other, Fraction):
            return self.position != other
        else:
            return Exception('Cannot != compare Position to type {0}.'.format(type(other)))
    
    def __gt__(self, other):
        from timemodel.offset import Offset
        if other is None:
            return False
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Fraction):
            return self.position > other
        if isinstance(other, Position):
            return self.position > other.position
        if isinstance(other, Offset):
            return self.position > other.offset

    def __ge__(self, other):
        if isinstance(other, Position):
            return self.position >= other.position
        else:
            return self.position >= other
    
    def __add__(self, other):
        from timemodel.duration import Duration
        from timemodel.offset import Offset
        if isinstance(other, Fraction) or isinstance(other, int):
            return Position(self.position + other)
        elif isinstance(other, float):
            return Position(self.position + Fraction(other))
        elif isinstance(other, Duration):
            return Position(self.position + other.duration)
        elif isinstance(other, Offset):
            return Position(self.position + other.offset)
        else:
            raise Exception('+ operator: cannot add {0} type {1} to position'.format(other, type(other)))
        
    def __radd__(self, other):
        return self + other
        
    def __iadd__(self, other):
        return self + other       
        
    def __sub__(self, other):
        from timemodel.duration import Duration
        from timemodel.offset import Offset
        if isinstance(other, Fraction) or isinstance(other, int):
            return Position(self.position - other)
        if isinstance(other, float):
            return Position(self.position - Fraction(other))
        elif isinstance(other, Position):
            return Duration(self.position - other.position)
        elif isinstance(other, Duration):
            return Position(self.position - other.duration)
        elif isinstance(other, Offset):
            return Position(self.position - other.offset)
        else:
            raise Exception('Cannot subtract type {0} from position', type(other))
        
    def __isub__(self, other):
        return self - other
    
    def __rsub__(self, other):
        return -self.__sub__(other)
        
    def __neg__(self):
        return Position(-self.position)
    
    def __mul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            return Position(self.position * other)
        elif isinstance(other, float):
            return Position(self.position * Fraction(other))
        else:
            raise Exception('+ operator: cannot add {0} type {1} to position'.format(other, type(other)))
        
    def __imul__(self, other):
        if isinstance(other, Fraction) or isinstance(other, int):
            return Position(self.position * other)
        if isinstance(other, float):
            return Position(self.position * Fraction(other))
        else:
            raise Exception('Cannot subtract type {0} from position', type(other)) 
        
    def __rmul__(self, other):
        return self * other
        
    def __str__(self):
        return str(self.position)
