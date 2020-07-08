from collections import OrderedDict


class DiscreteFunction(object):
    """
    Class implementation of a function between two discrete sets.  The two sets, domain and range are determined
    by the map itself.
    """

    def __init__(self, init_map=None):
        """
        Constructor.
        :param init_map: Initialization dictionary.
        """
        self._map = OrderedDict()

        if init_map is not None:
            if not isinstance(init_map, dict):
                raise Exception('initialize {0} must be a list or set of pairs'.format(init_map))
            self._map = init_map.copy()

    @property
    def domain(self):
        return set(self._map.keys())

    @property
    def range(self):
        return set(self._map.values())

    @property
    def map(self):
        return self._map.copy()

    def __getitem__(self, key):
        if key not in self._map:
            return None
        return self._map[key]

    def __setitem__(self, key, value):
        if key is None:
            raise Exception('\'None\' is illegal key.')
        self._map[key] = value

    def __delitem__(self, key):
        if key is None:
            raise Exception('\'None\' is illegal key.')
        if key not in self._map:
            raise Exception('{0} not in map.'.format(key))
        del self._map[key]
