"""

File: abstract_note.py

Purpose: AbstractNote, the root class behind all note constructs

"""
from abc import ABCMeta, abstractmethod
from timemodel.offset import Offset
from timemodel.position import Position
from fractions import Fraction


class AbstractNote(object):
    """
    A root class for all note and note grouping classes.
    
    The following are properties
    parent: The parent of an AbstractNote within an AbstractNote hierarchy, ref. AbstractNoteCollective.
    relative_position: A Position noting the whole note time onset of the note in it immediate collection.
    contextual_reduction_factor: The multiplicative factor imposed by a structure downward in the hierarchy.
    """
    
    NOTES_ADDED_EVENT = 'Notes added to line'
    NOTES_REMOVED_EVENT = 'Notes removed from line'
    
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__parent = None
        self.__relative_position = Offset(0)
        self.__contextual_reduction_factor = Fraction(1)
    
    @property
    def parent(self):
        return self.__parent
        
    @parent.setter
    def parent(self, parent):
        self.__parent = parent
        
    @property
    def relative_position(self):
        return self.__relative_position
    
    @relative_position.setter
    def relative_position(self, relative_position):
        self.__relative_position = relative_position
        
    @property
    def contextual_reduction_factor(self):
        return self.__contextual_reduction_factor
    
    @contextual_reduction_factor.setter
    def contextual_reduction_factor(self, contextual_reduction_factor):
        self.__contextual_reduction_factor = contextual_reduction_factor        
                
    @property
    def duration(self):
        raise NotImplementedError('define duration in subclass to use this base class')
    
    def reverse(self):
        raise NotImplementedError('users must define reverse() to use this base class')
    
    def get_original_parent(self):
        p = self.parent
        last_known_parent = p
        
        while True:
            if p is None:
                return last_known_parent
            last_known_parent = p
            p = p.parent
            
    def get_absolute_position(self):
        """
        Find the absolute position of this abstract note in its contextual tree
        """
        n = self
        p = Position(0)
        while True:
            p += n.relative_position
            n = n.parent
            if n is None:
                break
        return p           
           
    @abstractmethod
    def get_all_notes(self):
        raise NotImplementedError('users must define get_all_notes to use this base class')
    
    @staticmethod
    def print_structure(note, indent=0):
        from structure.note import Note
        from structure.beam import Beam
        from structure.beam import Tuplet
        from structure.line import Line
        if isinstance(note, Note):
            print('{0}Note {1} off {2} f={3} {4}'.format(indent*' ', str(note), note.relative_position,
                                                         note.contextual_reduction_factor,
                                                         'T' if note.is_tied_to else ''))
        elif isinstance(note, Beam):
            print('{0}Beam dur {1} off {2} f={3}'.format(indent*' ', note.duration, note.relative_position,
                                                         note.contextual_reduction_factor))
            for n in note.sub_notes:
                AbstractNote.print_structure(n, indent + 4)
        elif isinstance(note, Tuplet):
            print('{0}Tuplet dur {1} off {2} f={3}'.format(indent*' ', note.duration, note.relative_position,
                                                           note.contextual_reduction_factor))
            for n in note.sub_notes:
                AbstractNote.print_structure(n, indent + 4)
        elif isinstance(note, Line):
            print('{0}Line dur {1} off {2} f={3}'.format(indent*' ', note.duration, note.relative_position,
                                                         note.contextual_reduction_factor))
            for n in note.sub_notes:
                AbstractNote.print_structure(n, indent + 4)
        else:
            print('unknown type {0}'.format(type(note)))

    def clone(self):
        from structure.beam import Beam
        from structure.tuplet import Tuplet
        from structure.note import Note
        from structure.line import Line
        from timemodel.duration import Duration
        cpy = None
        if isinstance(self, Beam):
            cpy = Beam()
            for s in self.sub_notes:
                s_prime = s.clone()
                cpy.append(s_prime)
        elif isinstance(self, Tuplet):
            cpy = Tuplet(self.unit_duration, self.unit_duration_factor)
            for s in self.sub_notes:
                s_prime = s.clone()
                cpy.append(s_prime)
        elif isinstance(self, Note):
            d = Duration(self.base_duration.duration / self.contextual_reduction_factor)
            cpy = Note(self.diatonic_pitch if self.diatonic_pitch is not None else None, d, self.num_dots)
        elif isinstance(self, Line):
            cpy = Line(None, self.instrument)
            for s in self.sub_notes:
                s_prime = s.clone()
                cpy.pin(s_prime, s.relative_position)

        return cpy
