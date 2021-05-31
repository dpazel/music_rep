"""

File: event_sequence.py

Purpose: Defines a list of Events ordered by Event.time.  

"""
from timemodel.event import Event
from misc.ordered_map import OrderedMap


class EventSequence(object):
    """
    A class to collect a sequence of Event's ordered (increasing) by the Event's time value.
    The class contains the following event accounting structures:
    1) OrderedMap: ordering the events by time in a map that provides a floor() function.
    2) successor: a dict that maps events to successors.
    3) predecessor: a dict that maps events to predecessors.
    4) first: first event in the event sequence.
    5) last: last event in the event sequence.
    """

    def __init__(self, event_list=None):
        """
        Constructor.
        
        Args:
          event_list:  Any of None, a single Event, or a list of Events.
        """
        self.ordered_map = OrderedMap()
        
        self._successor = {}
        self._predecessor = {}
        self.__first = None
        self.__last = None
        
        if event_list:
            self.add(event_list)
    
    @property       
    def sequence_list(self):
        return list(self.ordered_map.get(x) for x in self.ordered_map.keys())
    
    @property
    def is_empty(self):
        return self.ordered_map.is_empty()
    
    def floor(self, time):
        return self.ordered_map.floor(time)
    
    def event(self, index):
        return self.ordered_map.get(index)
    
    def floor_event(self, time):
        floor_position = self.floor(time)
        return self.event(floor_position) if floor_position else None
    
    @property
    def first(self):
        return self.__first
    
    @property
    def last(self):
        return self.__last
    
    def add(self, new_members):
        """
        Add any of a single Event or a list of Events.
        
        Args:
          new_members: Any of a single Event or a list of events
        """
                
        if isinstance(new_members, list):
            mem_set = new_members
            inputt = [(e.time, e) for e in new_members]

        else:
            mem_set = [new_members]
            inputt = [(new_members.time, new_members)]
           
        for m in mem_set:
            if self.ordered_map.has_reverse(m):
                raise Exception('{0} already a member of sequence.'.format(m))  
            if not isinstance(m, Event):
                raise Exception('{0} is not an event.'.format(m)) 
            
        for i in inputt:
            if i[1].time not in self.ordered_map:
                self._add_successor_predecessor_maps(i[1])
            else:
                self._update_successor_predecessor_maps(i[1])
            self.ordered_map.insert(i[0], i[1])                  
        
    def remove(self, members): 
        """
        Remove any of a single Event or a list of Events already in the sequence.
        
        Args:
          members: Any of a single Event or a list of Events already in the sequence.
        """
        if isinstance(members, list):
            for member in members:
                self.remove(member)
        else:
            if not self.ordered_map.has_reverse(members):
                raise Exception('{0} not a member of sequence'.format(members))            
            self._remove_successor_predecessor_maps(members)
            self.ordered_map.remove_key(self.ordered_map.reverse_get(members))  
            
    def move_event(self, event, new_time):
        """
        Method to move event in sequence to a new time.
        
        Args:
          event: (Event) to move
          new_time: the new time setting for the event
        """
        if self.event(event.time) != event:
            raise Exception('Given event at time {0} not in sequence'.format(event.time))
        self.remove(event)
        event.time = new_time
        self.add(event)
            
    def _add_successor_predecessor_maps(self, event):
        fl_key = self.floor(event.time)
        if fl_key:
            a = self.event(fl_key)
            b = self._successor[a]  # could be None  event is between a and b
            self._successor[a] = event
            self._successor[event] = b
            self._predecessor[event] = a
            if b:
                self._predecessor[b] = event
            else:
                self.__last = event
        else:  # this event has to come first
            if self.__first:
                self._successor[event] = self.__first
                self._predecessor[self.__first] = event
                self._predecessor[event] = None
                self.__first = event
            else:
                self.__first = self.__last = event
                self._successor[event] = None
                self._predecessor[event] = None
            
    def _update_successor_predecessor_maps(self, event):
        e = self.event(event.time)
        self.remove(e)
        self._add_successor_predecessor_maps(event)
        pass
    
    def _remove_successor_predecessor_maps(self, event):
        a = self._predecessor[event]
        b = self._successor[event]
        del self._successor[event]
        del self._predecessor[event]
        if a:
            self._successor[a] = b
        else:
            self.__first = b
        if b:
            self._predecessor[b] = a
        else:
            self.__last = a
        
    def clear(self):
        self.ordered_map.clear()
        self._successor.clear()
        self._predecessor.clear()
        
    def successor(self, event):
        return self._successor[event] if event in self._successor else None
    
    def predecessor(self, event):
        return self._predecessor[event] if event in self._predecessor else None
        
    def __str__(self):
        return ', '.join(str(x) for x in self.sequence_list)
    
    def print_maps(self):
        print('---------')
        if self.__first:
            print('first={0}'.format(self.__first))
        else:
            print('first=None')
        if self.__first:
            print('last={0}'.format(self.__last))
        else:
            print('last=None')
        
        print('Successor:')
        for i in self._successor.items():
            print('   {0} --> {1}'.format(i[0].object if i[0] else 'None', i[1].object if i[1] else 'None'))

        print('Predecessor:')
        for i in self._predecessor.items():
            print('   {0} --> {1}'.format(i[0].object if i[0] else 'None', i[1].object if i[1] else 'None'))
