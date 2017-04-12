"""

File: ordered_map.py

Purpose: Defines a map whose key set is ordered.  This allows the definition of a floor function to 
         find a lower key to a specified key value.

"""
from collections import OrderedDict


class OrderedMap(object):
    """
    OrderedMap defines a dict whose key is ordered.
    """
    
    def __init__(self, inputt=None):
        """
        Constructor
        Args:
           inputt: A list or dict or OrderedMap.
        """
        if inputt is not None:
            if isinstance(inputt, list):
                self.od = OrderedDict(sorted(inputt, key=lambda t: t[0]))
                self.reverse_dict = {value: key for (key, value) in inputt}
            elif isinstance(inputt, dict) or isinstance(inputt, OrderedMap):
                self.od = OrderedDict(sorted(inputt.items(), key=lambda t: t[0]))
                self.reverse_dict = {value: key for (key, value) in inputt.items()}
            else:
                raise Exception('Cannot construct OrderedMap from type {0}'.format(type(inputt)))
        else:
            self.od = OrderedDict()
            self.reverse_dict = {}
            
    def get(self, index):
        return self.od[index]
    
    def __getitem__(self, index):
        return self.od[index]

    def __len__(self):
        return len(self.od)
    
    def is_empty(self):
        return len(self.od) == 0
    
    def reverse_get(self, value):
        """
        For a given object value find the key value that maps to it. 
        """
        return self.reverse_dict[value]
    
    def has_reverse(self, value):
        return value in self.reverse_dict
    
    def has_key(self, key):
        return key in self.od

    def __contains__(self, key):
        return key in self.od
    
    def keys(self):
        return self.od.keys()
    
    def insert(self, index, value):
        self.od[index] = value
        self.od = OrderedDict(sorted(self.od.items(), key=lambda t: t[0]))
        self.reverse_dict[value] = index
        
    def merge(self, inputt):
        """
        Merge a list of tuples, list, or OrderedMap.
        
        Args:
          inputt: A tuple list, dict, or OrderedMap.
          
        Returns:
          An OrderedMap that holding entries, a combination of self and inputt.
        """
        if inputt is not None:
            if isinstance(inputt, list):
                temp = dict(inputt)
                temp.update(self.od)
                self.od = OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
                for i in inputt:
                    self.reverse_dict[i[1]] = i[0]
            elif isinstance(inputt, dict) or isinstance(inputt, OrderedMap):
                temp = inputt.copy()
                temp.update(self.od)
                self.od = OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
                for i in inputt.items():
                    self.reverse_dict[i[1]] = i[0]
            else:
                raise Exception('Cannot merge OrderedMap from type {0}'.format(type(inputt)))  
            
    def copy(self):
        return OrderedMap(self.od.items())     
    
    def update(self, other_dict):
        self.od.update(other_dict) 
        self.od = OrderedDict(sorted(self.od.items(), key=lambda t: t[0]))
        for i in other_dict.items():
            self.reverse_dict[i[1]] = i[0]
        
    def remove_key(self, key):
        if key in self.od:
            value = self.od[key]
            del self.od[key]
            del self.reverse_dict[value]

    def clear(self):
        self.od = OrderedDict()
        self.reverse_dict = {}        
        
    def items(self):
        """
        Return all items in the ordered dictionary, each in tuple form (key, value).
        :return:
        """
        return self.od.items()

    def value_items(self):
        """
        Return all items in the ordered dictionary, but only the value in same order as self.items().
        :return:
        """
        return [x[1] for x in self.items()]

    def floor(self, key):
        key_index = self.floor_calc(key)
        if key_index is None:
            return None

        alist = self.od.keys()
        return alist[key_index]

    def ceil(self, key):
        key_index = self.floor_calc(key)

        alist = self.od.keys()
        if key_index is None:
            if self.is_empty():
                return None
            if key < alist[0]:
                return alist[0]
            if key_index == len(alist) - 1:
                return None
        return None if key_index >= len(alist) - 1 else alist[key_index + 1]

        
    #  Think of it as searching on N semi-closed intervals instead of searching on points.
    #  For N points there are N-1 sections., indexed 0 --> N-2,
    #       with the interval being represented by the lower point index.
    #  The critical test is seeing if 'item' is within the interval that starts with midpoint
    def floor_calc(self, key):
        """
        For a key find the highest map key less than the given key.
        
        Args:
          key: the input key for which we want to find the floor key in the map.
          
        Returns:
          the floor key, or None if none is found.
        """
        if self.is_empty():
            return None
                
        alist = self.od.keys()
        num_pts = len(alist)
        num_sections = num_pts - 1
   
        if key >= alist[num_pts - 1]:
            return num_pts - 1
        if key < alist[0]:
            return None
    
        first = 0
        last = num_sections - 1
        found = -1
    
        while first <= last and found == -1:
            midpoint = (first + last)//2
            if alist[midpoint + 1] > key >= alist[midpoint]:
                found = midpoint
                break
            if key < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    
        return found
    
    def floor_entry(self, item):
        """
        For a key find the highest map key less than given key, and its mapped value.
        
        Args:
          item: the input key for which we want to find the floor key and the mapped value.
          
        Returns:
          (floor_key, mapped_value)  or (None, None) if floor fails.
        """
        floor_key = self.floor(item)  
        if floor_key is None:
            return None, None
        return floor_key, self.od[floor_key]

    def ceil_entry(self, item):
        """
        For a key find the lowest map key greater than given key, and its mapped value.

        Args:
          item: the input key for which we want to find the ceil key and the mapped value.

        Returns:
          (ceil_key, mapped_value)  or (None, None) if ceil fails.
        """
        ceil_key = self.ceil(item)
        if ceil_key is None:
            return None, None
        return ceil_key, self.od[ceil_key]