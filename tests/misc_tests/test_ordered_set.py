import unittest

from misc.ordered_set import OrderedSet

class test_object(object):
    def __init__(self, ord):
        self.ord = ord

    def ord_value(self):
        return self.ord

    def __repr__(self):
        return str(self.ord)

class TestOrderedSet(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ordering(self):
        s1 = OrderedSet()
        for i in range(1, 10):
            s1.add(test_object(i))
        objects = [t.ord_value() for t in s1]
        assert objects == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_union(self):
        s1 = OrderedSet()
        for i in range(1, 10):
            s1.add(test_object(i))

        s2 = OrderedSet()
        for i in range(100, 110):
            to = test_object(i)
            s2.add(to)

        s = s1.union(s2)
        objects = [t.ord_value() for t in s]
        assert objects == [1, 2, 3, 4, 5, 6, 7, 8, 9, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

    def test_remove(self):
        s = OrderedSet()
        fone = None
        fmid = None
        flast = None
        for i in range(1, 10):
            item = test_object(i)
            if i == 1:
                fone = item
            elif i == 6:
                fmid = item
            elif i == 9:
                flast = item
            s.add(item)

        s.remove(fmid)
        s.remove(flast)
        s.remove(fone)
        objects = [t.ord_value() for t in s]
        assert objects == [2, 3, 4, 5, 7, 8]

    def test_copy(self):
        s = OrderedSet()
        for i in range(1, 10):
            to = test_object(i)
            s.add(to)

        s1 = s.copy()
        assert id(s1) != id(s)

        objects = [t.ord_value() for t in s1]
        assert objects == [1,2, 3, 4, 5, 6, 7, 8, 9]

    def test_constructor(self):
        s = OrderedSet([1, 2, 3, 4, 5])
        items = [item for item in s]

        assert items == [1, 2, 3, 4, 5]
