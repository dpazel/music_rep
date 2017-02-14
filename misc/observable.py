"""

File: observable.py

Purpose: Observable in an observer pattern.  In short, provides a means for
         an object to provide notification of event based on something 'happening' to it.

"""


class Observable(object):
    """
    Implementation of observer in Observer pattern.  The class defines a means
    of notifying clients of changes to the observable, as calls to the observer's 
    'notification' method.
    """

    def __init__(self):
        """
        Constructor
        """
        self.observers = set()
        
    def register(self, observer):
        """
        Register the observer to the observable.
        
        Args:
          observer: instance of Observer that gets notification
        Note: gets added to observers list, and is user responsibility to remove.
        """
        from misc.observer import Observer
         
        if not isinstance(observer, Observer):
            raise Exception('Argument is not an observer')       
        if observer not in self.observers:
            self.observers.add(observer)
            
    def deregister(self, observer):
        """
        Deregister observer as observer.
        
        Args:
          observer: instance of Observer that is removed for notification
          
        """
        from misc.observer import Observer
                
        if not isinstance(observer, Observer):
            raise Exception('Argument is not an observer')
        try:
            self.observers.remove(observer)  
        except (KeyError, AttributeError):
            # invalid observer, or the observers cleared
            pass
        
    def deregister_all(self):
        """
        Deregister all observers.
        """
        while len(self.observers) != 0:
            self.deregister(self.observers.pop())
        
    def update(self, message_type, message=None, data=None):
        """
        update is called whenever an event of importance should be noted by 
        all the observable's clients.
        
        Args:
          message_type: (any type) a message indicating the type of event.
          message: (string) any associated message about the event.
          data: (any type) any associated data about the event.
        """
        for observer in self.observers:
            observer.notification(self, message_type, message, data)
