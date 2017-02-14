"""

File: beam.py

Purpose: Defines the Beam note construct.

"""
from abstract_note_collective import AbstractNoteCollective
from note import Note
from tuplet import Tuplet

from fractions import Fraction
from timemodel.duration import Duration


class Beam(AbstractNoteCollective):
    """
    Beam is a grouping operation, having a set scaling ratio of 1/2, but unbounded aggregate duration.
    
    The basic idea of a beam is that for a stand alone beam, you can only add Note's of duration 1/4 or less.  
    That duration is retained under the beam.  
    However when a beam is added to a beam, it takes an additional reduction factor of 1/2.
    
    Note that these factors aggregate multiplicatively through self.contextual_reduction_factor
    """
    
    FACTOR = Fraction(1, 2)
    NOTE_QUALIFIER_DURATION = Duration(1, 4)

    def __init__(self, abstract_note_list=list()):
        """
        Constructor
        
        Args: 
          abstract_note_list: list of notes, beams, and tuplets to add consecutively under the beam.
        """
        AbstractNoteCollective.__init__(self)
        
        self.append(abstract_note_list)   
        
    @property
    def duration(self):
        """
        This is an override of AbstractNoteCollective.duration.
        Tuplet and Beam override this to do a simple summation of linearly layed out notes and subnotes.
                 The reason is that the layout algorithm of these subclasses cannot use the realtive_position
                 attribute as the algorithm determines that.
        """
        d = Duration(0)
        for note in self.sub_notes:
            d += note.duration
        return d    
       
    def append(self, notes):
        """
        Append a set of abstract notes to the beam
        
        Args:
          notes: either a list of notes or a single note to add to the beam.
        """
        if isinstance(notes, list):
            for n in notes:
                self.append(n)
            return
        self.add(notes, len(self.sub_notes))
        
    def add(self, note, index):
        """
        Beams can only add less than 1/4 notes, and arbitrary beams and tuplets.
        Only added beams incur a reduction factor of 1/2
        For collective notes, always apply the factor.
        """
        if note.parent is not None:
            raise Exception('Cannot add note already assigned a parent')
        if index < 0 or index > len(self.sub_notes):
            raise Exception('add note, index {0} not in range[0, {1}]'.format(index, len(self.sub_notes)))

        if isinstance(note, Note):
            if note.base_duration >= Duration(1, 4):
                raise Exception(
                    "Attempt to add note with duration {0} greater than or equal to {1}".
                    format(note.duration, Beam.NOTE_QUALIFIER_DURATION))
            new_factor = self.contextual_reduction_factor
        elif isinstance(note, Beam):
            new_factor = self.contextual_reduction_factor * Beam.FACTOR
        elif isinstance(note, Tuplet):
            new_factor = self.contextual_reduction_factor
        else:
            raise Exception('illegal type {0}'.format(type(note)))
        
        self.sub_notes.insert(index, note)
        note.parent = self
        note.apply_factor(new_factor)
        # The following call will adjust layout from this point right upward
        self.upward_forward_reloc_layout(note)  
                       
        # see if prior note is tied, and if so, break the tie.
        first_note = note
        if not isinstance(note, Note):   
            first_note = note.get_first_note()
        prior = first_note.prior_note()   
        if prior is not None and prior.is_tied_to:
            prior.untie()  
         
        # notify up the tree of what has changed
        self.notes_added([note]) 
   
    def __str__(self):
        base = 'Beam(Dur({0})Off({1})f={2})'.format(self.duration, self.relative_position,
                                                    self.contextual_reduction_factor)
        s = base + '[' + (']' if len(self.sub_notes) == 0 else '\n')
        for n in self.sub_notes:
            s += '  ' + str(n) + '\n'
        s += ']' if len(self.sub_notes) != 0 else ''
        return s
