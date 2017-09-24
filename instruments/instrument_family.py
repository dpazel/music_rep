"""

File: instrument_family.py

Purpose: Defines a genera for a particular instrument, usually based on key, e.g. Clarinet having Clarinet Bb, Eb, etc. 

"""
from instruments.instrument_base import InstrumentBase


class InstrumentFamily(InstrumentBase):
    """
    Class designating an specific instrument genera, e.g. Clarinet, having  Clarinet Bb, Eb, etc. 
    """

    def __init__(self, name, parent=None):
        """
        Constructor.
        
        Args:
          name: (String) name of family, e.g. Clarinets
        """
        InstrumentBase.__init__(self, name, parent)
        
        self.__instruments = []
    
    @property 
    def instruments(self):
        return list(self.__instruments)   
       
    def add_instrument(self, instrument):
        self.__instruments.append(instrument)
        
    def __str__(self):
        return '{0}'.format(self.name)
