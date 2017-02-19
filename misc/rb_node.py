"""

File: rb_node.py

Purpose: Defines an implementation of a node in an interval tree,
         a means to determine which intervals intersect at point.

Note: Implementation is based on Cormen, et. al. Algorithms - in particular red-black trees and interval trees.

"""
from misc.interval import Interval


class IntervalInfo(object):
    """
    Class defining object to hold the direct association of an interval to some object value.
    """
    
    def __init__(self, interval, value, rb_node):
        """
        Constructor
        
        Args:
        interval: type Interval, interval of interest.
        value: object value associated with the interval.
        rb_node: for this information.
        """
        self.__interval = interval
        self.__value = value
        
        # Some may indicate this is inappropriate.  Actually this value should only be visible to
        # IntervalTree and RBNode.  It is the best way to facilitate a node deletion.  With this,
        # We pass IntervalInfo (as received by a query say) to a delete method which can delete the node directly.
        self.__rb_node = rb_node
    
    @property
    def interval(self):
        return self.__interval
    
    @property
    def value(self):
        return self.__value
    
    @property
    def rb_node(self):
        return self.__rb_node
    
    def __str__(self): 
        return "({0} : {1})".format(self.interval, self.value)


class RBNode(object):
    """
    Defines an implementation of a node in an interval tree
    """
    Red, Black = range(2)

    def __init__(self, interval=None, value=None, interval_tree=None):
        """
        Constructor.

        Args:
            interval: coverage Interval
            value: value mapped to
            interval_tree: parent IntervalTree
        """
        self.__interval = interval
        self.__key = interval.lower if interval else None
        self.__value = value
      
        self.__min = interval.lower if interval else None
        self.__max = interval.upper if interval else None
        
        self.__color = RBNode.Black

        self.__parent = None
        
        self.interval_tree = interval_tree
        
        self.__id = 1 if self.interval_tree is None else self.interval_tree.gen_node_id()
        
        self.__nil = interval_tree.nil if interval_tree else None
        self.__left = self.nil
        self.__right = self.nil

    @property
    def interval(self):
        return self.__interval
    
    @property
    def key(self):
        return self.__key
    
    @key.setter
    def key(self, k):
        self.__key = k
    
    @property
    def value(self):
        return self.__value
    
    @property
    def min(self):
        return self.__min
    
    @property
    def max(self):
        return self.__max
    
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color):
        self.__color = color
    
    @property
    def left(self):
        return self.__left
    
    @left.setter
    def left(self, node):
        self.__left = node
    
    @property
    def right(self):
        return self.__right
    
    @right.setter
    def right(self, node):
        self.__right = node
               
    @property
    def parent(self):
        return self.__parent
    
    @parent.setter
    def parent(self, node):
        self.__parent = node
        
    @min.setter
    def min(self, newmin):
        self.__min = newmin
        
    @max.setter
    def max(self, newmax):
        self.__max = newmax
        
    @property
    def nil(self):
        return self.__nil
    
    @property
    def id(self):
        return self.__id
    
    def coverage(self):
        if self.min is None or self.max is None:
            return None
        return Interval(self.min, self.max)
    
    def query_point(self, index, answer):
        """
        Query for all intervals that intersect a point.
        
        Args:
          index: Number to be queried about
          answer: List to be filled with answers
          
        Returns:
          The answer list of IntervalInfo's
        """
        if self.interval.contains(index):
            answer.append(IntervalInfo(self.interval, self.value, self))
        if self.left != self.nil and self.left.max > index >= self.left.min:
            self.left.query_point(index,  answer)
        if self.right != self.nil and self.right.max > index >= self.right.min:
            self.right.query_point(index,  answer)
        return answer
            
    def query_interval(self, interval, answer):
        """
        Query for all intervals that intersect a given interval.
        
        Args:
          interval: The Interval to check intersection against
          answer:  The return list of IntervalInfo's
        
        Returns:
          The answer list of IntervalInfo's
        """
        if Interval.intersects(self.interval, interval):
            answer.append(IntervalInfo(self.interval, self.value, self))
        if self.left != self.nil and (self.left.min <= interval.upper and self.left.max > interval.lower): 
            self.left.query_interval(interval,  answer)

        if self.right != self.nil and (self.right.min <= interval.upper and self.right.max > interval.lower):
            self.right.query_interval(interval,  answer)
        return answer
    
    def query_interval_start(self, interval, answer):
        """
        Find all intervals that start in the given interval, and only those.
        
        Args:
          interval: The interval to collect interval starts on.
          answer: The return list of IntervalInfo's
          
        Returns:
          The answer list of IntervalInfo's
        """
        if interval.contains(self.interval.lower):
            answer.append(IntervalInfo(self.interval, self.value, self))
                       
        if self.left != self.nil and (self.left.min <= interval.upper and self.left.max > interval.lower): 
            self.left.query_interval_start(interval,  answer)

        if self.right != self.nil and (self.right.min <= interval.upper and self.right.max > interval.lower):
            self.right.query_interval_start(interval,  answer)
        return answer

    def intervals(self, interval_list):
        if self.left != self.nil:
            self.left.intervals(interval_list)
        interval_list.add(self.interval)
        if self.right != self.nil:
            self.right.intervals(interval_list)
        return interval_list
    
    def intervals_and_values(self, info_list):
        if self.left != self.nil:
            self.left.intervals_and_values(info_list)
     
        info_list.add(IntervalInfo(self.interval, self.value, self))
        if self.right != self.nil:
            self.right.intervals_and_values(info_list)
      
        return info_list
    
    def apply_update(self):
        x = self
        while x != self.nil:
            x.update_min_max()
            x = x.parent
            
    def update_min_max(self):
        maxx = self.interval.upper
        if self.left != self.nil:
            maxx = self.left.max if maxx < self.left.max else maxx
    
        if self.right != self.nil:
            maxx = self.right.max if maxx < self.right.max else maxx
     
        self.max = maxx
      
        minn = self.interval.lower
        if self.left != self.nil:
            minn = self.left.min if minn > self.left.min else minn

        if self.right != self.nil:
            minn = self.right.min if minn > self.right.min else minn
      
        self.min = minn
        
    def left_rotate(self):  # assumes x, swaps with x.right
        x = self
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.interval_tree.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
      
        y.left = x
        x.parent = y
        self.apply_update()

    def right_rotate(self):  # assume y, swaps with y.left
        y = self
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y

        x.parent = y.parent
        if y.parent == self.nil:
            self.interval_tree.root = x
        else:
            if y == y.parent.right:
                y.parent.right = x
            else:
                y.parent.left = x

        x.right = y
        y.parent = x
      
        self.apply_update()
        
    def node_minimum(self):
        x = self
        while self.left != self.nil:
            x = self.left()
        return x
    
    def node_maximum(self):
        x = self
        while self.right != self.nil:
            x = self.right()
        return x
    
    def node_successor(self):
        if self.right != self.nil:
            return self.right.node_minimum()
        y = self.parent
        x = self
        while y != self.nil and x == y.right:
            x = y
            y = y.parent
        return y   
            
    def delete_node(self, rb_node):
        """
        Best description is in Cormen ( p. 251):
        
        The procedure for deleting a given node z from a binary search tree takes as an argument a pointer to z.
        The procedure considers the three cases shown in Figure 13.4.  If z has no children, we modify its parent p[z]
        to replace z with NIL as its child.  If the node has only a single child, we "splice out" z by making a 
        new link between its child and its parent.  Finally, if the node has two children,
        we splice out z's successor y,
        which has no left child ... and replace the contents of z with the contents of y. 
        
        In order to key prior search results valid (ref. IntervalInfo), we ALWAYS want to get rid of z.  So in the third
        case, we really want to replace rb_node with its successor, moving left, right from rb_node to the successor and
        re-assigning the parentage.
        """
        if rb_node.left == self.nil or rb_node.right == self.nil:
            x = rb_node.left if rb_node.left != self.nil else rb_node.right
            x.parent = rb_node.parent
            if rb_node.parent == self.nil:
                self.interval_tree.root = x
            else:
                if rb_node == rb_node.parent.left:
                    rb_node.parent.left = x
                else:
                    rb_node.parent.right = x
            # Please test to see if this fixes spans
            if rb_node.parent != self.nil:
                rb_node.parent.apply_update()
            if x != self.nil and rb_node.color == RBNode.Black:
                self._rb_delete_fixup(x)
        else:
            y = rb_node.node_successor()
            x = y.left if y.left != self.nil else y.right 
            if x != self.nil:
                x.parent = y.parent if y.parent != rb_node else y
            if y.parent == self.nil:
                self.interval_tree.root = x
            else:
                if y.parent != rb_node:
                    if y == y.parent.left:
                        y.parent.left = x
                    else:
                        y.parent.right = x  
                    
            # replace rb_node with y
            
            y.left = rb_node.left 
            if y.left != self.nil:
                y.left.parent = y
            y.right = rb_node.right if y.parent != rb_node else y.right
            if y.right != self.nil:
                y.right.parent = y
            y.color = rb_node.color
            y.parent = rb_node.parent
            if rb_node.parent == self.nil:
                self.interval_tree.root = y
            else:
                if rb_node == rb_node.parent.left:
                    rb_node.parent.left = y
                else:
                    rb_node.parent.right = y
            # Please test to see if this fixes spans
            # I think the span for y should be computed immediately, then y.apply_update()
            if y != self.nil:
                y.apply_update()
            if y.color == RBNode.Black and x != self.nil:
                self._rb_delete_fixup(x)    

    def _rb_delete_fixup(self, x):
        while x != self.interval_tree.root and x.color == RBNode.Black:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RBNode.Red:
                    w.color = RBNode.Black
                    x.parent.color = RBNode.Red
                    x.parent.left_rotate() 
                    w = x.parent.right
                if w.left.color == RBNode.Black and w.right.color == RBNode.Black:
                    w.color = RBNode.Red
                else:
                    if w.right.color == RBNode.Black:
                        w.left.color = RBNode.Black
                        w.color = RBNode.Red
                        w.right_rotate()
                    w.color = x.parent.color
                    x.parent.color = RBNode.Black
                    w.right.color = RBNode.Black
                    x.parent.left_rotate()
                    x = self.interval_tree.root
            else:
                w = x.parent.left
                if w.color == RBNode.Red:
                    w.color = RBNode.Black
                    x.parent.color = RBNode.Red
                    x.parent.right_rotate() 
                    w = x.parent.left
                if w.right.color == RBNode.Black and w.left.color == RBNode.Black:
                    w.color = RBNode.Red
                else:
                    if w.left.color == RBNode.Black:
                        w.right.color = RBNode.Black
                        w.color = RBNode.Red
                        w.left_rotate()
                    w.color = x.parent.color
                    x.parent.color = RBNode.Black
                    w.left.color = RBNode.Black
                    x.parent.right_rotate()
                    x = self.interval_tree.root

        x.color = RBNode.Black      
        
    def print_tree(self):
        s = ''
        if self.left != self.nil:
            s = s + self.left.print_tree()   # self.left.print_tree()

        s = s + str(self) + '\n'
      
        if self.right != self.nil:
            s = s + self.right.print_tree()  # self.right.print_tree();
        return s
    
    def __str__(self): 
        return "[{0}] key={1} interval={2} c={3} parent=[{4}] span=[{5}, {6}] --> [{7}, {8}]".format(
          self.id, self.key, self.interval, 'B' if self.color == RBNode.Black else 'R',
          self.parent.id, self.min, self.max,
          'null' if self.left is None else self.left.id,
          'null' if self.right is None else self.right.id)
