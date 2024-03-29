import unittest

from misc.interval_tree import IntervalTree
from misc.rb_node import RBNode
from misc.interval import Interval
from fractions import Fraction

from unittest.mock import MagicMock


class TestRBNode(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_access(self):
        mock = MagicMock(spec=IntervalTree)
        interval = Interval(2, 4)
        value = Fraction(2, 5)
        node = RBNode(interval, value, mock)
        
        assert node.interval == interval
        assert node.key == interval.lower
        assert node.value == value
        assert node.min == 2
        assert node.max == 4
        
        assert not node.parent
        assert node.left == node.nil
        assert node.right == node.nil
