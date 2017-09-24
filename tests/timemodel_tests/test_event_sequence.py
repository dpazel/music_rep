import unittest

from timemodel.event_sequence import EventSequence
from timemodel.event import Event
from timemodel.position import Position


class TestEventSequence(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_successor(self):
        es = EventSequence()
        p1 = Event('str_1', Position(1, 2))
        es.add(p1)
        print(es)
        assert es.successor(p1) is None
        
        p2 = Event('str_2', Position(1))
        es.add(p2)
        print(es)
        assert es.successor(p1) == p2
        assert es.successor(p2) is None
        
        p3 = Event('str_2', Position(3, 4))
        es.add(p3)
        print(es)
        assert es.successor(p1) == p3
        assert es.successor(p3) == p2
        assert es.successor(p2) is None
        
    def test_basic_succ_pred_sequence(self):
        events = [Event(3, Position(0)), 
                  Event(6, Position(1, 2)), 
                  Event(2, Position(3, 4)), 
                  Event(7, Position(1)), 
                  Event(8, Position(3, 2)) 
                  ]
        es = EventSequence(events)
        print(es)
        
        assert es.successor(events[0]) == events[1]
        assert es.successor(events[1]) == events[2]
        assert es.successor(events[2]) == events[3]
        assert es.successor(events[3]) == events[4]
        assert es.successor(events[4]) is None
        
        assert es.predecessor(events[4]) == events[3]
        assert es.predecessor(events[3]) == events[2]
        assert es.predecessor(events[2]) == events[1]
        assert es.predecessor(events[1]) == events[0]
        assert es.predecessor(events[0]) is None
        
        assert es.first == events[0]
        assert es.last == events[4]
        
        es = EventSequence()
        for i in reversed(range(len(events))):
            es.add(events[i])
        print(es)
        
        assert es.successor(events[0]) == events[1]
        assert es.successor(events[1]) == events[2]
        assert es.successor(events[2]) == events[3]
        assert es.successor(events[3]) == events[4]
        assert es.successor(events[4]) is None
        
        assert es.predecessor(events[4]) == events[3]
        assert es.predecessor(events[3]) == events[2]
        assert es.predecessor(events[2]) == events[1]
        assert es.predecessor(events[1]) == events[0]
        assert es.predecessor(events[0]) is None
        
        assert es.first == events[0]
        assert es.last == events[4]
        
        es = EventSequence()
        for i in [2, 4, 1, 3, 0]:
            es.add(events[i])
        print(es)
        
        assert es.successor(events[0]) == events[1]
        assert es.successor(events[1]) == events[2]
        assert es.successor(events[2]) == events[3]
        assert es.successor(events[3]) == events[4]
        assert es.successor(events[4]) is None
        
        assert es.predecessor(events[4]) == events[3]
        assert es.predecessor(events[3]) == events[2]
        assert es.predecessor(events[2]) == events[1]
        assert es.predecessor(events[1]) == events[0]
        assert es.predecessor(events[0]) is None
        
        assert es.first == events[0]
        assert es.last == events[4]
        
        es.remove(events[3])
        print('remove object 7')
        print(es)
        print(es.print_maps())
        
        assert es.successor(events[0]) == events[1]
        assert es.successor(events[1]) == events[2]
        assert es.successor(events[2]) == events[4]
        assert es.successor(events[4]) is None
        
        assert es.predecessor(events[4]) == events[2]
        assert es.predecessor(events[2]) == events[1]
        assert es.predecessor(events[1]) == events[0]
        assert es.predecessor(events[0]) is None
        
        assert es.first == events[0]
        assert es.last == events[4]
        
        new_event = Event(23, Position(3, 4))
        print('update object 2 to 23')

        es.add(new_event)
        print(es)
        es.print_maps()       
        assert es.successor(events[0]) == events[1]
        assert es.successor(events[1]) == new_event
        assert es.successor(new_event) == events[4]
        assert es.successor(events[4]) is None
        
        assert es.predecessor(events[4]) == new_event
        assert es.predecessor(new_event) == events[1]
        assert es.predecessor(events[1]) == events[0]
        assert es.predecessor(events[0]) is None
        
        assert es.first == events[0]
        assert es.last == events[4]
        
        es.move_event(new_event, Position(1, 8))
        print('move (23, 3/4) to (23, 1/8)')
        print(es)
        es.print_maps()
        
        assert es.successor(events[0]) == new_event
        assert es.successor(new_event) == events[1]
        assert es.successor(events[1]) == events[4]
        assert es.successor(events[4]) is None
        
        assert es.predecessor(events[4]) == events[1]
        assert es.predecessor(events[1]) == new_event
        assert es.predecessor(new_event) == events[0]
        assert es.predecessor(events[0]) is None
        
        assert es.first == events[0]
        assert es.last == events[4]

if __name__ == "__main__":
    unittest.main()
