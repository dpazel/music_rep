import unittest

from misc.observable import Observable
from misc.observer import Observer


class MyObservable(Observable):
    COUNT_UPDATE = 35
    COUNT_UPDATE_MSG = 'Count Update'
    
    def __init__(self, name, count):
        Observable.__init__(self)
        self.__name = name
        self.__count = count
       
    @property
    def count(self):
        return self.__count
    
    @property
    def name(self):
        return self.__name
    
    @count.setter
    def count(self, count):
        self.__count = count
        self.update(MyObservable.COUNT_UPDATE, MyObservable.COUNT_UPDATE_MSG, self.count)
    
            
class MyObserver(Observer):
    def __init__(self, name):
        Observer.__init__(self)
        self.__name = name
        self.__last_observed = 0
       
    @property
    def name(self):
        return self.__name  
    
    @property 
    def last_observed(self):
        return self.__last_observed
    
    def notification(self, observable, message_type, message=None, data=None):
        print 'Observer {0} saw value Updated to {1} in \'{2}\''.format(self.name, data, observable.name)
        self.__last_observed = data
        

class TestObservable(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_general(self):
        o = MyObservable('thing', 5)
        b = MyObserver('b')
        o.register(b)
        
        o.count = 10
        assert b.last_observed == 10
        
        c = MyObserver('c')
        d = MyObserver('d')
        o.register(c)
        o.register(d)
        
        o.count = 35
        assert b.last_observed == 35
        assert c.last_observed == 35
        assert d.last_observed == 35
        
        o.deregister(b)
        o.count = 40
        assert b.last_observed != 40
        assert c.last_observed == 40
        assert d.last_observed == 40
        o.deregister(c)
         
        o.deregister_all()
        o.count = 50
        assert b.last_observed != 50
        assert c.last_observed != 50
        assert d.last_observed != 50        


if __name__ == "__main__":
    unittest.main()
