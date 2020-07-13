import collections.abc
from collections import OrderedDict

'''
OrderedSet: A set that retains order of insertion.
'''


class OrderedSet(collections.abc.MutableSet):

    def __init__(self, iterable=None):
        self.dict = OrderedDict()
        if iterable is not None:
            for item in iterable:
                self.add(item)

    def add(self, item):
        if item not in self.dict:
            self.dict[item] = 0

    def __len__(self):
        return len(self.dict)

    def __contains__(self, item):
        return item in self.dict

    def __iter__(self):
        for item in self.dict.keys():
            yield item

    def discard(self, elem):
        if elem in self.dict:
            self.dict.pop(elem, None)

    def copy(self):
        return OrderedSet(self)

    def union(self, iterable):
        s = self.copy()
        if iterable is not None:
            s |= iterable
        return s

    def __repr__(self):
        return str(self)

    def __str__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))
