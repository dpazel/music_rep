"""

File: tuplet.py

Purpose: Defines Line note construct

"""
from structure.abstract_note_collective import AbstractNoteCollective
from structure.note import Note
from structure.beam import Beam
from structure.tuplet import Tuplet
from timemodel.offset import Offset
from misc.interval import Interval
from fractions import Fraction

from timemodel.position import Position


class Line(AbstractNoteCollective):
    """
    Line is a grouping operation having unbounded duration and constant scaling factor 1.
    """
    
    LINE_NOTES_ADDED_EVENT = 'Line notes added to line'
    LINE_NOTES_REMOVED_EVENT = 'Line notes removed from line'

    def __init__(self, abstract_note_list=None, instrument=None):
        """
        Constructor
        
        Args: 
          abstract_note_list: list of or one of notes, beams, and tuplets to add consecutively under the line.
        """
        AbstractNoteCollective.__init__(self)
        
        self.__instrument = instrument
        
        # map note --> articulation setting
        self.articulation_map = {}

        # This is still dangerous.  We used to use append.
        # Problem when voice is called passing an arg, then Voice.pin is called before proper initialization.
        #    The issue is that Voice designer has to know NOT to pass an arg.  How to get around?
        if abstract_note_list:
            self.pin(abstract_note_list)
            
    @property
    def instrument(self):
        return self.__instrument
    
    @instrument.setter
    def instrument(self, new_instrument):
        self.__instrument = new_instrument
        
    @property
    def duration(self):
        return self.length()

    def append(self, note_structure):
        self.pin(note_structure, Offset(self.duration.duration))
                
    def pin(self, note_structure, offset=Offset(0)):
        """
        Given a note_structure (Line, Note, Tuplet, Beam), make it an immediate child to this line.
        If it is a list, the members are added in note sequence, with offset being adjusted appropriately.
        
        Args:
          note_structure: (List of Line, Note, Tuplet, Beam) to add
          offset:  (Offset), of the first in list or given structure.
        """

        if not isinstance(offset, Offset):
            raise Exception('Offset parameter in pin() must be of type Offset, not \'{0}\'.'.format(type(offset)))
        if isinstance(note_structure, list):
            for n in note_structure:
                self._append_note(n, offset)
                offset += n.duration
        else:
            self._append_note(note_structure, offset)
            
        # sort by relative offset    Pins can happen any where, this helps maintains some sequential order to the line 
        sorted(self.sub_notes, key=lambda n1: n1.relative_position)
            
        self.update(Line.LINE_NOTES_ADDED_EVENT, None, note_structure) 
            
    def _append_note(self, note, offset):
        if not isinstance(note, Beam) and not isinstance(note, Tuplet) and not isinstance(note, Note) \
                and not isinstance(note, Line):
            raise Exception('Cannot add instance of {0} to Line'.format(type(note)))
        self.sub_notes.append(note)
        note.parent = self 
        note.relative_position = offset 
        
    def _validate_(self, note):
        pass
        
    def unpin(self, note_structure):
        if isinstance(note_structure, list):
            for n in note_structure:
                self._remove_note(n)
        else:
            self._remove_note(note_structure)
            
        # sort by relative offset    Unpins can happen any where, this helps maintains some sequential order to the line 
        sorted(self.sub_notes, key=lambda n1: n1.relative_position)
            
        self.update(Line.LINE_NOTES_REMOVED_EVENT, None, note_structure) 
        
    def _remove_note(self, note):
        if not isinstance(note, Beam) and not isinstance(note, Tuplet) and not isinstance(note, Note) \
                and not isinstance(note, Line):
            raise Exception('Cannot remove instance of {0} to Line'.format(type(note)))
        if note not in self.sub_notes:
            raise Exception('Con only remove notes in line {0)'.format(note))
        self.sub_notes.remove(note)
        note.parent = None   
        
    def clear(self):
        notification_list = list(self.sub_notes)
        for note in notification_list:
            self.sub_notes.remove(note)
            note.parent = None 
        self.update(Line.LINE_NOTES_REMOVED_EVENT, None, notification_list)        
        
    def __str__(self):
        base = 'Line(Dur({0})Off({1})f={2})'.format(self.duration, self.relative_position,
                                                    self.contextual_reduction_factor)
        s = base + '[' + (']' if len(self.sub_notes) == 0 else '\n')
        for n in self.sub_notes:
            s += '  ' + str(n) + '\n'
        s += ']' if len(self.sub_notes) != 0 else ''
        return s
    
    def upward_forward_reloc_layout(self, abstract_note):
        pass

    def sub_line(self, sub_line_range=None):
        """
        Take a sub-range (time) of this line, and build a new line with notes that begins within that range
        :param sub_line_range: numeric interval to check for inclusion.
        :return: (sub-line, onset of original (Position), duration of sub-line)

        Note: The sub_line is not guaranteed to have the same length as the line, as sub_line is constructed only of
        the notes contained withing sub_line_range, starting with the first note found.
        """
        sub_line_range = Interval(Fraction(0), self.duration.duration) if sub_line_range is None else sub_line_range

        new_line = Line(None, self.instrument)

        first_position = None
        for s in self.sub_notes:
            s_excluded = Line._all_start_in(s, sub_line_range)
            if s_excluded == 1:
                if first_position is not None:
                    offset = Offset(s.get_absolute_position().position - first_position)
                else:
                    first_position = s.get_absolute_position().position
                    offset = Offset(0)
                s_prime = s.clone()
                new_line.pin(s_prime, offset)
            else:
                if s_excluded == -1:
                    raise Exception("Line range {0} must fully enclose sub-structures: {1}.".format(sub_line_range, s))

        return new_line, Position(first_position) if first_position is not None else Position(0), new_line.duration

    @staticmethod
    def _all_start_in(note_structure, sub_line_range):
        """
        See if all notes in note_structure start within range.
        :param note_structure:
        :param sub_line_range: Numeric interval to check for inclusion.
        :return: 1 if covers fully, 0 if fully excluded, -1 if partially excluded
        """
        notes = note_structure.get_all_notes()
        num_notes_excluded = 0
        for n in notes:
            if not sub_line_range.contains(n.get_absolute_position().position):
                num_notes_excluded = num_notes_excluded + 1
        return 1 if num_notes_excluded == 0 else 0 if num_notes_excluded == len(notes) else -1
