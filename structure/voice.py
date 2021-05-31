"""

File: voice.py

Purpose: A voice is a Line, but has an associated instrument and an interval tree for note searches relative to 
         whole note time.

"""
from misc.interval_tree import IntervalTree
from misc.interval import Interval
from structure.line import Line
from structure.dynamics import Dynamics
from timemodel.duration import Duration
from timemodel.offset import Offset
from timemodel.dynamics_event_sequence import DynamicsEventSequence

from misc.observer import Observer
from timemodel.dynamics_event import DynamicsEvent
from timemodel.position import Position


class Voice(Observer):
    """
    Voice is a Line with two key attributes:
    1) Instrument that 'plays' this voice.
    2) Interval tree to enable fast searches for notes in the Voice.
    
    Voice can only add Lines, and the interval tree covers all the notes in the contained lines.
    """

    def __init__(self, instrument):
        """
        Constructor.
        
        Note: there are several interesting questions here.
           1) should Line.__init__ be called first.  Because the init coult call overridden methods, e.g. duration
           2) should Voice be limited to Line membership only?
        """
        Observer.__init__(self)
        
        self.__instrument = instrument
                  
        self.__lines = []
        self.interval_tree = IntervalTree()  
        
        # map notes to their articulation
        self.articulation_map = {}  
        
        # Sequence of event related to setting dynamics
        self.__dynamics_sequence = DynamicsEventSequence()
           
    @property
    def lines(self):
        return list(self.__lines)
    
    @property
    def instrument(self):
        return self.__instrument
    
    @property
    def duration(self):
        return self.length()
    
    def length(self):
        from misc.utility import convert_to_numeric
        from fractions import Fraction
        last = Fraction(0)
        for l in self.lines:
            ep = convert_to_numeric(l.relative_position + l.length())
            if ep > last:
                last = ep
        return Duration(last) 
    
    def assign_articulation(self, note, articulation):
        if not self.note_belongs_to_voice(note):
            raise Exception("Note {0} does not belong to voice".format(note))
        self.articulation_map[note] = articulation
        
    def get_articulation(self, note):
        if note in self.articulation_map:
            return self.articulation_map[note]
        return None
    
    def get_velocity(self, position):
        dynamics_event = self.dynamics_sequence.floor_event(position)
        if not dynamics_event:
            return Dynamics.DEFAULT_DYNAMICS_VELOCITY()
        if isinstance(dynamics_event, DynamicsEvent):
            return dynamics_event.velocity()
        else:
            next_dfe = self.dynamics_sequence.successor(dynamics_event)
            return dynamics_event.velocity(position, next_dfe.time if next_dfe else Position(self.length().duration))
    
    @property
    def dynamics_sequence(self):
        return self.__dynamics_sequence
    
    def coverage(self):
        """
        Returns the WNT coverage interval for voice.
        """
        return self.interval_tree.root.coverage()
        
    def pin(self, line, offset=Offset(0)):
        """
        Overrides Line.pin.  The differences is that only a Line can be added with notes starting at 'offset'
        to the beginning of the line.
        
        Args:
          line:  Line to be added
          offset:  (Offset) into Voice to add the line.
        """
        if not isinstance(line, Line):
            raise Exception('Voice can only pin Line\'s, {0} received'.format(type(line)))
        
        if line not in self.__lines:
            self.__lines.append(line)
            line.register(self)
        else:
            self._remove_notes_from_tree(line.get_all_notes())
            
        line.relative_position = offset
        
        # add all the individual notes to the interval_tree
        #  NOTE: don't do this twice!!!
        self._add_notes_to_tree(line.get_all_notes())
        
    def unpin(self, line):
        if not isinstance(line, Line):
            raise Exception('Voice can only unpin Line\'s, {0} received'.format(type(line)))
        if line not in self.__lines:
            raise Exception('Voice can only unpin lines it owns')
        self.__lines.remove(line)
        line.relative_position = Offset(0)
        line.deregister(self)
        
        self._remove_notes_from_tree(line.get_all_notes())
            
    def _add_notes_to_tree(self, notes):
        for note in notes:
            
            # check of note is in range of the voice's instrument..
            if note.diatonic_pitch.chromatic_distance < self.instrument.sounding_low.chromatic_distance or \
               note.diatonic_pitch.chromatic_distance > self.instrument.sounding_high.chromatic_distance:
                raise Exception('Note {0} not in instrument {1} sounding range'.format(note, self.instrument)) 
            
            interval = Interval(note.get_absolute_position(), 
                                note.get_absolute_position() + note.duration)
            self.interval_tree.put(interval, note)
            
    def _remove_notes_from_tree(self, notes):
        # remove all intervals from the old line
        for note in notes:
            interval = Interval(note.get_absolute_position().position, 
                                note.get_absolute_position().position + note.duration.duration)
            result = self.interval_tree.find_exact_interval(interval)
            for interval_info in result:
                if interval_info.value == note:
                    self.interval_tree.delete(interval_info)  
                    
            if note in self.articulation_map:
                del self.articulation_map[note]      
            
    def get_notes_by_interval(self, interval, line=None):
        """
        Get all notes in the voice whose position/duration intersect with a given interval.
        
        Args:
          interval: given Interval.
          line: optional Line to restrict search to.
        Returns:
          List of notes satisfying query.
        """
        if line:
            if line not in self.__lines:
                return []
            notes = self.get_notes_by_interval(interval)
            return_val = [n for n in notes if Voice._find_line_by_note(n) == line]
            return_val.sort(key=lambda x: x.get_absolute_position())
            return return_val 
        else:
            result = self.interval_tree.query_interval(interval)
            notes = [info.value for info in result]
            notes.sort(key=lambda x: x.get_absolute_position())
            return notes
        
    def get_notes(self, start_position, end_position, line=None):
        """
        Get all notes in explicit interval given as lower/upper bounds, [)
        
        Args:
          start_position: Position of the start of the interval (inclusive)
          end_position: Position of the end of the interval (non-inclusive)
          line: Optionsl Line to restrict search to:
          
        Returns:
          List of notes satisfying query
        """
        return self.get_notes_by_interval(Interval(start_position, end_position), line)
    
    def get_notes_starting_in_interval(self, interval, line=None):
        """
        Get all notes that start in the given interval.
        
        Args:
          interval: Interval wherein return notes must begin.
          line: Optional Line to restrict search to.
        Returns:
          list of notes satisfying query.
        """
        if line:
            if line not in self.__lines:
                return []
            notes = self.get_notes_starting_in_interval(interval)
            return_val = [n for n in notes if Voice._find_line_by_note(n) == line]
            return_val.sort(key=lambda x: x.get_absolute_position())
            return return_val
        else:
            result = self.interval_tree.query_interval_start(interval)
            notes = [info.value for info in result]
            notes.sort(key=lambda x: x.get_absolute_position())
            return notes 

    @staticmethod
    def _find_line_by_note(note):
        p = note.parent
        while p is not None:
            if isinstance(p, Line):
                return p
            p = p.parent
        return None
    
    def note_belongs_to_voice(self, note):
        p = note.parent
        while p is not None:
            if p in self.__lines:
                return True
            p = p.parent
        return False

    def get_all_notes(self):
        notes = []
        for line in self.__lines:
            notes.extend(line.get_all_notes())
        return notes
    
    def notification(self,  observable, message_type, message=None, data=None):
        from structure.abstract_note import AbstractNote     
        if isinstance(observable, Line):
            if message_type == Line.LINE_NOTES_ADDED_EVENT: 
                self._add_notes_to_tree(Voice._extract_all_notes(data))
            elif message_type == Line.LINE_NOTES_REMOVED_EVENT:
                self._remove_notes_from_tree(Voice._extract_all_notes(data))
            elif message_type == AbstractNote.NOTES_ADDED_EVENT:
                self._add_notes_to_tree(Voice._extract_all_notes(data))

    @staticmethod
    def _extract_all_notes(data):
        notes = []
        note_input = data if isinstance(data, list) else [data]
        for s in note_input:
            notes.extend(s.get_all_notes())    
        return notes    
    
    def __str__(self):
        base = 'Voice(Dur({0}))'.format(self.duration)
        s = base + '[' + (']' if len(self.lines) == 0 else '\n')
        for n in self.lines:
            s += '  ' + str(n) + '\n'
        s += ']' if len(self.lines) != 0 else ''
        return s
