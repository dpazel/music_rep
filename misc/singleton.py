
class Singleton(object):
    """
    This is a class that implements singleton for its subclasses.
    The technique is based on a variant of other techniques found in:
    http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

    The technique is simply to build a map of classes to their unique instances.
    The first time called for some particular
    class the class is mapped to the instance.  On other class to the same class, the mapped instance is returned.
    Classes that use this must:
    1) Add Singleton as a superclass.
    2) Have this signature for the constructor: __init__(self, *args, **kwargs)
    """
    _instances = {}

    @classmethod
    def instance(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls]  = cls(*args, **kwargs)
        return cls._instances[cls]

