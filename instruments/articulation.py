"""

File: articulation.py

Purpose: Define a representative class for articulations.

"""


class Articulation(object):
    """
    Define a representative class for articulations.
    """

    def __init__(self, name):
        """
        Constructor.

        Args:
            name: String name of articulation.
        """
        self.__name = name
        
    @property
    def name(self):
        return self.__name
    
    def __str__(self):
        return '{0}'.format(self.name)
