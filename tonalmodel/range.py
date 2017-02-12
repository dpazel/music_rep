"""

File: range.py

Purpose: Defines an inclusive range of integers.

"""


class Range(object):
    """
    Range class encapsulates an inclusive range of (integer) values
    """

    def __init__(self, start_index, end_index):
        """
        Constructor.
        
        Args:
          start_index: beginning numeric (integer).
          end_index: last and included numeric (integer)
          
        Note: Throws exception if begin precedes start, not not integer input.
        """
        if not isinstance(start_index, int):
            raise Exception("Start value in range must be integer {0}".format(type < start_index))
        if not isinstance(end_index, int):
            raise Exception("End value in range must be integer {0}".format(type < end_index))
        if end_index < start_index:
            raise Exception('Illegal range {0} > {1}'.format(start_index, end_index))
        
        self.__start_index = start_index
        self.__end_index = end_index
        
    @property
    def start_index(self):
        return self.__start_index
    
    @property
    def end_index(self):
        return self.__end_index
    
    def __str__(self):
        return 'R[{0}, {1}]'.format(self.start_index, self.end_index)
    
    def size(self):
        """
        Return the number of integer values in range.
        """
        return self.end_index - self.start_index + 1
    
    def is_inbounds(self, index):
        """
        Determine if index is in bounds to this range.
        
        Args:
          index: numeric value
        Returns:
          boolean for inclusion.
        Note: unpredictable result for non-numeric
        return index >= self.start_index and index <= self.end_index
        """
        return self.end_index >= index >= self.start_index
