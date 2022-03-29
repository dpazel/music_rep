"""

File: observer.py

Purpose: Observer in an observer pattern.  In short, a client to an observable
         that receives notification of event based on something 'happening' to the observable.

"""
from abc import ABCMeta, abstractmethod


class Observer(object):
    """
    Observer (client) to an Observable
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Constructor.
        """
 
    @abstractmethod
    def notification(self, observable, message_type, message=None, data=None):
        """
        The method an observer must implement that is called whenever an event of interest happens to the
        observable.
        
        Args:
          observable: (Observable) the observable issuing the notification.
          message_type: (any type) a message indicating the type of event.
          message: (string) any associated message about the event.
          data: (any type) any associated data about the event.
        """
        pass   