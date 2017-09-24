"""

File: instrument_class.py

Purpose: Defines a major category of instruments in the instrument category.  In this case, 
         is used to identity broad instrument types, e.g. stringw, woodwinds, bass, percussion, keyboards.

"""
from instruments.instrument_base import InstrumentBase


class InstrumentClass(InstrumentBase):
    """
    Class to identify a broad instrument type, e.g.  stringw, woodwinds, bass, percussion, keyboards.
    """

    def __init__(self, name, parent=None):
        """
        Constructor.
        
        Args:
          name: (String) name of class, e.g. woodwinds, strings
        """
        
        InstrumentBase.__init__(self, name, parent)
        
        self.__families = []
            
    @property
    def families(self):
        return list(self.__families)
    
    def add_family(self, family):
        self.__families.append(family)
        
    def __str__(self):
        return '{0}'.format(self.name)
