import unittest
from misc.interval_tree import IntervalTree
from misc.interval import Interval
import logging


class MyObject(object):
    def __init__(self, idd):
        self.__idd = idd
        
    @property
    def idd(self):
        return self.__idd
    
    def __str__(self):
        return str(self.idd)

    
class TestInterval(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_tree(self):
        print('simple tree text')
        tree = IntervalTree()
        tree.put(Interval(4,   7),        MyObject(1))
        tree.put(Interval(6.0, 7.000001), MyObject(1))
        print(tree)
    
        result = tree.query_point(5.9)
        assert result
        assert len(result) == 1
        assert result[0].interval == Interval(4, 7)
    
        result = tree.query_point(6.0)
        assert result
        assert len(result) == 2
        assert result[0].interval == Interval(4, 7)
        assert result[1].interval == Interval(6.0, 7.000001)
    
        result = tree.query_point(7.0000001)
        assert result
        assert len(result) == 1
        assert result[0].interval == Interval(6.0, 7.000001)

    def test_duplicate_interval(self):
        print('test duplicate interval')
        tree = IntervalTree()
        tree.put(Interval(4.0, 7.0),  MyObject(1))   
        tree.put(Interval(4.0, 7.0),  MyObject(1))
    
        # We want two results - same (equals) interval, two different objects.
        result = tree.query_point(5.9)
        assert result
        assert len(result) == 2
        assert result[0].interval == Interval(4.0, 7.0)
        assert result[1].interval == Interval(4.0, 7.0)
        assert result[0].value != result[1].value
        
        print(tree)
        
    def test_problem_interval(self):
        print('test problem interval')
        tree = IntervalTree()
        tree.put(Interval(0.0, .5),  MyObject(1))   
        print(tree)
        print('---')
        tree.put(Interval(.5, 1.0),  MyObject(1))
        print(tree)
        print('---')
        tree.put(Interval(1.0, 1.25),  MyObject(1))
        print('Tree for test problem interval')
        print(tree)
        
    def test_overlapping_stair(self):
        tree = IntervalTree()
        for i in range(1, 4):
            tree.put(Interval(i, i + 3), MyObject(i))
        print('Tree for test overlapping stair')
        print(tree)
        
        result = tree.query_point(1.5)
        assert result
        assert len(result) == 1
        assert sum(x.value.idd for x in result) == 1
        
        result = tree.query_point(2.5)
        assert result
        assert len(result) == 2
        assert sum(x.value.idd for x in result) == 3
        
        result = tree.query_point(3.5)
        assert result
        assert len(result) == 3
        assert sum(x.value.idd for x in result) == 6
        
        result = tree.query_point(4.5)
        assert result
        assert len(result) == 2
        assert sum(x.value.idd for x in result) == 5
        
        result = tree.query_point(5.5)
        assert result
        assert len(result) == 1
        assert sum(x.value.idd for x in result) == 3
        
        result = tree.query_point(6.5)
        assert len(result) == 0
        
        result = tree.query_interval(Interval(2, 3))
        assert len(result) == 2
        assert sum(w.value.idd for w in result) == 3
        print(', '.join((str(w) for w in result)))
        
        result = tree.query_interval(Interval(3, 4))
        assert len(result) == 3
        assert sum(w.value.idd for w in result) == 6
        print(', '.join((str(w) for w in result)))
        
    def test_delete_node(self):
        print('Delete node test')
        tree = IntervalTree()
        for i in range(1, 4):
            tree.put(Interval(i, i + 3), MyObject(i))
        print(tree)
            
        result = tree.query_point(3.5)
        assert result
        assert len(result) == 3
        print(', '.join(('[' + str(w.value.idd) + '] ' + str(w) for w in result)))
        assert sum(x.value.idd for x in result) == 6
        
        print('Deleting [{0}] {1}'.format(result[0].value.idd, result[0]))
        tree.delete(result[0])       
        print(tree)
        
        result = tree.query_point(3.5)
        assert result
        assert len(result) == 2
        
        # single node delete test
        print('Single node delete test')
        tree = IntervalTree()
        tree.put(Interval(3, 5), MyObject(5))
        print(tree)
        
        result = tree.query_point(3)
        assert len(result) == 1
        tree.delete(result[0])
        print(tree)
        result = tree.query_point(3)
        assert len(result) == 0
        
    def test_delete_with_one_child(self):
        print('Test delete with one child')
        tree = IntervalTree()
        tree.put(Interval(15, 30), MyObject(1))
        tree.put(Interval(5, 10), MyObject(2))

        tree.put(Interval(16, 30), MyObject(3))
        tree.put(Interval(18, 25), MyObject(5))
        tree.put(Interval(20, 40), MyObject(4))
        tree.put(Interval(23, 50), MyObject(6))      
        
        # 20 should have a right node only
        print(tree)
        result = tree.query_point(20)
        f = None
        for r in result:
            if r.rb_node.key == 20:
                f = r
                break
        assert f
        assert f.rb_node.left == tree.nil
        assert f.rb_node.right != tree.nil
        
        tree.delete(f)
        print(tree)
        result = tree.query_point(20)
        f = None
        for r in result:
            if r.rb_node.key == 20:
                f = r
                break
        assert not f
        
    def test_delete_with_two_child(self):
        print('Test delete with two children')
        tree = IntervalTree()
        tree.put(Interval(15, 30), MyObject(1))
        tree.put(Interval(5, 10), MyObject(2))

        tree.put(Interval(16, 30), MyObject(3))
        tree.put(Interval(18, 25), MyObject(5))
        tree.put(Interval(20, 40), MyObject(4))
        tree.put(Interval(23, 50), MyObject(6))      
        
        # 18 should have left and right
        print(tree)
        result = tree.query_point(18)
        f = None
        for r in result:
            if r.rb_node.key == 18:
                f = r
                break
        assert f
        assert f.rb_node.left != tree.nil
        assert f.rb_node.right != tree.nil
        
        tree.delete(f)
        print(tree)
        
        result = tree.query_point(18)
        f = None
        for r in result:
            if r.rb_node.key == 18:
                f = r
                break
        assert not f
        
    def test_delete_min_max(self):
        print('Test delete min max')
        tree = IntervalTree()
        tree.put(Interval(15, 30), MyObject(1))
        tree.put(Interval(5, 10), MyObject(2))

        tree.put(Interval(16, 30), MyObject(3))
        tree.put(Interval(18, 25), MyObject(5))
        tree.put(Interval(20, 40), MyObject(4))
        tree.put(Interval(23, 50), MyObject(6))      
        
        # 23 span is 23-50
        print(tree)
        result = tree.query_point(23)
        f = None
        for r in result:
            if r.rb_node.key == 23:
                f = r
                break
        assert f
        assert f.rb_node.key == 23
        
        tree.delete(f)
        print(tree)
        assert tree.root.max == 40
        
    def test_match_interval(self):
        print('Test match interval')
        
        tree = IntervalTree()
        tree.put(Interval(15, 30), MyObject(1))
        tree.put(Interval(5, 10), MyObject(2))

        tree.put(Interval(16, 30), MyObject(3))
        tree.put(Interval(18, 25), MyObject(5))
        tree.put(Interval(20, 40), MyObject(4))

        tree.put(Interval(23, 50), MyObject(6))
        
        result = tree.find_exact_interval(Interval(16, 30))  
        assert result is not None
        assert len(result) == 1
        
        assert result[0].interval == Interval(16, 30)   
        
        print(tree)


if __name__ == "__main__":
    unittest.main()

