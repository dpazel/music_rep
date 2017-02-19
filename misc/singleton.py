"""

File: singleton.py

Purpose: Defines a class whose subclasses will act like the singleton pattern.

"""


class Singleton(object):
    """
    This is a class that implements singleton for its subclasses.
    The technique is based on a variant of other techniques found in:
    http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    https://gist.github.com/werediver/4396488

    The technique is simply to build a map of classes to their unique instances.
    The first time called for some particular
    class the class is mapped to the instance.  On other class to the same class, the mapped instance is returned.
    """
    _instances = {}

    @classmethod
    def instance(cls):
        if cls not in cls._instances:
            cls._instances[cls]  = cls()
        return cls._instances[cls]

