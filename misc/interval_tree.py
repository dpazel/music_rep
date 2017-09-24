"""

File: interval_tree.py

Purpose: Defines an implementation of interval tree, a means to determine which intervals intersect at point.

Note: Implementation is based on Cormen, et. al. Algorithms - in particular red-black trees and interval trees.

"""

from misc.rb_node import RBNode
from fractions import Fraction
from timemodel.position import Position
import numbers 


class IntervalTree(object):
    """
    IntervalTree is a class that uses the RB-Tree algorithms, but modified to a useful search means over
    intervals over a real line.  This implementation is based on Cormen, et. al. Algorithms.
    Some modification were made to that algorithm to, for example, allow multiple node deletions.
    """

    def __init__(self):
        """
        Constructor.
        """
        
        # A nil RBNode is used in lieu of None as indicated in Corman that it
        # facilitates the algorithm details.
        self.__nil = RBNode()
        
        # And nil is currently the root.
        self.__root = self.nil
        
        self.__node_id_gen = 1
        
    def gen_node_id(self):
        # __node_gen_id is used to generate a unique identifying integer, per tree, per RBNode.
        self.__node_id_gen += 1
        return self.__node_id_gen
     
    @property
    def root(self):
        return self.__root
    
    @property
    def nil(self):
        return self.__nil
     
    @root.setter
    def root(self, root_node):
        self.__root = root_node 
        
    def _tree_insert(self, node):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
    
        node.parent = y
        if y == self.nil:
            self.root = node
        else:
            if node.key < y.key:
                y.left = node
            else:
                y.right = node
      
    def put(self, interval, value):
        node = RBNode(interval, value, self)
    
        self._tree_insert(node)
        node.apply_update()
    
        node.color = RBNode.Red
        while node != self.root and node.parent.color == RBNode.Red:
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if y != self.nil and y.color == RBNode.Red:
                    node.parent.color = RBNode.Black
                    y.color = RBNode.Black
                    node.parent.parent.color = RBNode.Red
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        node.left_rotate()
                    node.parent.color = RBNode.Black
                    node.parent.parent.color = RBNode.Red
                    node.parent.parent.right_rotate()
            else:
                y = node.parent.parent.left
                if y != self.nil and y.color == RBNode.Red:
                    node.parent.color = RBNode.Black
                    y.color = RBNode.Black
                    node.parent.parent.color = RBNode.Red
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        node.right_rotate()
                    node.parent.color = RBNode.Black
                    node.parent.parent.color = RBNode.Red
                    node.parent.parent.left_rotate()
    
        self.root.color = RBNode.Black 
        
        return node
        
    def query_point(self, point):
        """
        Query for all intervals that intersect a point.
        
        Args:
          point: Number to be queried about
          
        Returns:
          The answer list of IntervalInfo's
        """
        if self.root == self.nil:
            return []  
        return self.root.query_point(point, [])
  
    def query_interval(self, interval):
        """
        Query for all intervals that intersect a given interval.
        
        Args:
          interval: The Interval to check intersection against
        
        Returns:
          The answer list of IntervalInfo's
        """
        return self.root.query_interval(interval, [])
    
    def find_exact_interval(self, interval):
        """
        Find all results (intervals via IntervalInfo's) that match a given interval.
        
        Args:
          interval: Interval to find
        Returns:
          List of IntervalInfo's that match the interval exactly.
        """
        
        mid_value = (interval.upper + interval.lower) * Fraction(1, 2)
        mid = Position(mid_value) if isinstance(mid_value, numbers.Rational) or isinstance(mid_value, Fraction) else \
            mid_value

        results = self.query_point(mid)
        ret_results = []
        for result in results:
            if result.interval == interval:
                ret_results.append(result)
        return ret_results
    
    def query_interval_start(self, interval):
        """
        Find all results (intervals via IntervalInfo's that start in given interval
        
        Args:
          interval: Interval to find
        Returns:
          List of IntervalInfo's that start in given interval.
        """
        answer = []
        if self.root != self.nil:
            self.root.query_interval_start(interval, answer)
        return answer
    
    def delete(self, interval_info):
        """
        Delete an interval from the interval tree.  
        
        Args:
          interval_info: IntervalInfo that had been acquired from a search.
        """
        self.root.delete_node(interval_info.rb_node)
    
    def intervals(self): 
        return self.root.intervals([])

    def intervals_and_values(self):
        return self.root.intervals_and_values([])
    
    def tree_minimum(self):
        return self.root.node_minimum()
    
    def tree_maximum(self):
        return self.root.node_maximum()
      
    def print_tree(self):
        if not self.root:
            return ''
        base = 'root = [{0}] \n'.format(self.root.id)
        return base + self.root.print_tree()
    
    def __str__(self):
        return self.print_tree()
