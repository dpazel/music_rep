"""

File: abstract_note_collective.py

Purpose: Defines a base class behind all note aggregation structues, e.g. Beam, Tuplet, Line

"""

from structure.abstract_note import AbstractNote
from timemodel.offset import Offset
from timemodel.duration import Duration

from misc.observable import Observable
from misc.observer import Observer


class AbstractNoteCollective(AbstractNote, Observer, Observable):
    """
    This class is the root to classes that aggregate other abstract notes.  
    That attribute is self.sub_notes, a list of consecutive child notes to the collective.
    This in essence constructs a tree of notes.
    """

    def __init__(self):
        """
        Constructor
        """
        AbstractNote.__init__(self)
        
        Observable.__init__(self)
        Observer.__init__(self)
        
        self.sub_notes = []
        
    def cardinality(self):
        return len(self.sub_notes)
    
    def sub_notes(self):
        """
        Access a list of sub_notes
        
        Returns
          A new list containing the contents of self.sub_notes
          
          NOTE: fix, cannot treat as property due to note insertion (self.sub_notes.insert(...), but should 
                allow way to get a copy of self.sub_notes
        """
        lst = []
        lst.extend(self.sub_notes)
        return lst

    @property
    def duration(self):
        """
        This is effectively the same as length(), giving the length of the collection.
        However, Tuplet and Beam override this to do a simple summation of linearly layed out notes and subnotes.
                 The reason is that the layout algorithm of these subclasses cannot use the realtive_position
                 attribute as the algorithm determines that.
        """
        return self.length() 
     
    def length(self):
        from structure.note import Note
        from fractions import Fraction
        from misc.utility import convert_to_numeric
        d = Fraction(0)
        for n in self.sub_notes:
            d = max(d, convert_to_numeric(n.relative_position + (n.duration if isinstance(n, Note) else n.duration)))
        return Duration(d)
                  
    def downward_refactor_layout(self, incremental_factor):
        """
        Called by Tuplet, this method applies the incremental factor down the tree, adjusting 
        note duration accordingly.  At a Note, it calls apply_factor to make durational adjustments.
        Otherwise, it calls recursively.
        The method also rescales the relative positions of abstract notes.
        
        Args:
          incremental_factor: the multiplicative factor to apply downward.
        """
        from structure.note import Note
        
        self.contextual_reduction_factor *= incremental_factor
        relpos = Offset(0)
        for n in self.sub_notes:
            if isinstance(n, Note):
                n.apply_factor(incremental_factor)
            else:
                n.downward_refactor_layout(incremental_factor)
            n.relative_position = relpos
            relpos += n.duration
        
    def upward_forward_reloc_layout(self, abstract_note):   
        """
        Called by Beam on Beam content alteration, it climbs the tree upward and to the right.
        making relative position adjustments along the way.  It stops when it hits either a null parent
        or a tuplet.  Since tuplets will not change size, there is no need to proceed higher up the tree.
        However, at that top tuplet level, it is appropriate to call Tuplet.rescale() as the lower contents
        have changed and can affect the tuplet's rescaling factor.
        
        Args:
          abstract_note: the affected child note of self.sub_notes which causes the relocataion layout.
        """
        from structure.tuplet import Tuplet
        try:
            index = self.sub_notes.index(abstract_note)
        except ValueError:
            raise Exception('Could note location index for {0} in {1}'.format(abstract_note, type(self)))
        
        current_position = Offset(0) if index == 0 else \
            self.sub_notes[index - 1].relative_position + self.sub_notes[index - 1].duration
        for i in range(index, len(self.sub_notes)):
            self.sub_notes[i].relative_position = current_position
            current_position += self.sub_notes[i].duration
        
        # Once size no longer changes, no need to propagate
        if self.parent is not None and not isinstance(self.parent, Tuplet):
            self.parent.upward_forward_reloc_layout(self)
            
        if self.parent is not None and isinstance(self.parent, Tuplet):
            self.parent.rescale()
            
    def apply_factor(self, factor):
        """
        Recursively update the contextual reduction factor by a factor.
        This is typically called when a new note structure is added to an exiting structure to get the
        factors up to date.
        
        Args:
          factor: factor to be applied to self.contextual_reduction_factor.
        """
        for n in self.sub_notes:
            n.apply_factor(factor) 
        self.relative_position *= factor 
        self.contextual_reduction_factor *= factor            
            
    def get_all_notes(self):
        """
        Recursive method to get a list of all notes within a structure, in positional order.
        """
        notes = []    
        for abstract_note in self.sub_notes:
            notes.extend(abstract_note.get_all_notes())
                
        return notes
    
    def get_next_child(self, child):
        index = self.sub_notes.index(child)
        if index == -1:
            raise Exception('Could not find child {} in collective {1}'.format(child, self))
        if index >= len(self.sub_notes) - 1:
            return None
        return self.sub_notes[index + 1]
    
    def get_prior_child(self, child):
        index = self.sub_notes.index(child)
        if index == -1:
            raise Exception('Could not find child {} in collective {1}'.format(child, self))
        if index == 0:
            return None
        return self.sub_notes[index - 1]
    
    def get_first_note(self):
        from structure.note import Note
        if len(self.sub_notes) == 0:
            return None
        
        n = self.sub_notes[0]
        if isinstance(n, Note):
            return n
        return n.get_first_note()
    
    def get_last_note(self):
        from structure.note import Note
        if len(self.sub_notes) == 0:
            return None
        
        n = self.sub_notes[len(self.sub_notes) - 1]
        if isinstance(n, Note):
            return n
        return n.get_last_note()
    
    def reverse(self):
        # reverse recursively
        self.sub_notes.reverse()
        for n in self.sub_notes:
            n.reverse()
        
        # recompute the relative locations    
        current_position = Offset(0) 
        for n in self.sub_notes:
            n.relative_position = current_position
            current_position += n.duration
            
        # if we are at the top, parent == None, get all notes and reverse ties
        if self.parent is None:
            notes = self.get_all_notes()
            # see discussion why we cannot march forward nor backwards and just untie and tie.
            notes_to_tie = []
            for n in notes:
                if n.is_tied_to:
                    notes_to_tie.append(n.tied_to)
                    n.untie()
            for n in notes_to_tie:
                n.tie()
                
    @AbstractNote.parent.setter
    def parent(self, p):
        if self.parent:
            self.deregister(self.parent)  # make parent not observe me.
        AbstractNote.parent.fset(self, p)
        # super(AbstractNote, self.__class__).parent.fset(self, p)  ???
        if self.parent:
            self.register(self.parent)    # make the parent observe me

    def notes_added(self, note_list):  
        self.update(AbstractNote.NOTES_ADDED_EVENT, None, note_list)
             
    def notification(self,  observable, message_type, message=None, data=None):
        if message_type == AbstractNote.NOTES_ADDED_EVENT:
            self.update(AbstractNote.NOTES_ADDED_EVENT, None, data)
