"""

File: tuplet.py

Purpose: Defines Line note construct

"""
from structure.abstract_note_collective import AbstractNoteCollective
from structure.note import Note
from structure.beam import Beam
from structure.tuplet import Tuplet
from timemodel.offset import Offset


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
                
    def pin(self, note_structure, offset=Offset(0)):
        """
        Given a note_structure (Line, Note, Tuplet, Beam), make it an immediate child to this line.
        If it is a list, the members are added in note sequence, with offset being adjusted appropriately.
        
        Args:
          note_structure: (List of Line, Note, Tuplet, Beam) to add
          offset:  (Offset), of the first in list or given structure.
        """
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
