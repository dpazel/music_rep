"""

File: instrument_base.py

Purpose: Defines a base class for the instrument catalog tree.  Each node has this as a base class.

"""


class InstrumentBase(object):
    """
    This class is a base class for all classes in the instrument catalog tree.
    It takes case of details such as:
    *) Management of parent
    *) Holds the name as a property
    *) Holds the articulation set.
    
    The articulation is cumulative through parentage - using the tree with specifics at the lowest level
    and general articulations at the higher level.
    """

    def __init__(self, name, parent=None):
        """
        Constructor
        Args:
        name: (String)
        parent: (InstrumentBase) of the parent node; None is no parent.
        """
        self.__name = name
        self.__parent = parent
        
        self.__articulations = []
        
    @property
    def name(self):
        return self.__name
    
    @property
    def parent(self):
        return self.__parent
    
    def get_native_articulations(self):
        return list(self.__articulations)
    
    def add_articulation(self, articulation):
        self.__articulations.append(articulation)
        
    def extend_articulations(self, articulation_list):
        self.__articulations.extend(articulation_list)

    @property
    def articulations(self):
        return self.__articulations

    @articulations.setter
    def articulations(self, articulation_list):
        self.__articulations = list()
        self.__articulations.extend(articulation_list)

    def get_articulations(self):
        """
        Get the list of articulations from this level and up.
        """
        art_list = self.get_native_articulations()
        parent = self.parent
        while parent is not None:
            art_list.extend(parent.get_native_articulations())
            parent = parent.parent
            
        return art_list
