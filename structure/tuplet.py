"""
Created on Feb 13, 2016

File: tuplet.py

Purpose: Defines Tuplet note construct

@author: donald p pazel
"""
from structure.abstract_note_collective import AbstractNoteCollective
from structure.note import Note
from timemodel.duration import Duration


class Tuplet(AbstractNoteCollective):
    """
    Tuplet is a grouping operation having bounded duration but variable scale factor based on full content duration.
    The bounded duration is determined by two attributes;
    1) unit_duration: a Duration representing a base note value 
    2) unit_duration_factor: a numeric representing how many of the above the full duration should be.
    """

    def __init__(self, unit_duration, unit_duration_factor, abstract_note_list=None):
        """
        unit_duration x unit_duration_factor gives the full intended duration for the construct.
        tuplets have bounded duration but variable scale factor based on its contents 
        
        Args:
          unit_duration: a Duration representing a base note value, e.g. quarter note 
          unit_duration_factor: a numeric representing how many of the above the full duration should be.
          abstract_note_list: a list of abstract notes to append to the tuplet
          
        Note that these factors aggregate multiplicatively through self.contextual_reduction_factor (see rescale())
        """
        AbstractNoteCollective.__init__(self)
        
        self.__unit_duration = unit_duration
        self.__unit_duration_factor = unit_duration_factor

        if abstract_note_list is None:
            abstract_note_list = list()
        self.append(abstract_note_list)
        
    @property
    def unit_duration(self):
        return self.__unit_duration
    
    @property
    def unit_duration_factor(self):
        return self.__unit_duration_factor 
    
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
        Append one or a list of notest to the tuplet.

        :param notes: List or individual note
        :return:
        """
        if isinstance(notes, list):
            for n in notes:
                self.append(n)
            return
        elif isinstance(notes, Note) or isinstance(notes, AbstractNoteCollective):
            self.add(notes, len(self.sub_notes))
        
    def add(self, note, index):
        """
        Beams can only add less than 1/4 notes, and arbitrary beams and tuplets.
        Only added beams incur a reduction factor of 1/2
        For collective notes, always apply the factor.
        """
        from structure.beam import Beam
        if note.parent is not None:
            raise Exception('Cannot add note already assigned a parent')
        if index < 0 or index > len(self.sub_notes):
            raise Exception('add note, index {0} not in range[0, {1}]'.format(index, len(self.sub_notes)))
        
        if isinstance(note, Note):
            if note.base_duration >= 2 * self.unit_duration:
                raise Exception(
                    "Attempt to add note with duration {0} greater than or equal to {1}".format(note.duration,
                                                                                                2 * self.unit_duration))
        elif not isinstance(note, Beam) and not isinstance(note, Tuplet):
            raise Exception('illegal type {0}'.format(type(note)))
            
        self.sub_notes.insert(index, note)
        note.parent = self
        note.apply_factor(self.contextual_reduction_factor)
        self.rescale()
        
        # see if prior note is tied, and if so, break the tie.
        first_note = note
        if not isinstance(note, Note):   
            first_note = note.get_first_note()
            # If empty tuplet or beam added, not note to tie.
            if first_note is None:
                return
        prior = first_note.prior_note()   
        if prior is not None and prior.is_tied_to:
            prior.untie()  
            
        self.notes_added([note])  
        
    def rescale(self):
        """
        Rebuild the factors for the duration is right.
        Instead of setting the self.contextual_reduction_factor, we create an incremental factor that when applied to
        the contextual_reduction_factor give the correct new factor.
        This is preferred since the incremental can be applied downward the tree
        in a straight forward way, as a contextual adjustment multiplicative factor.
        """
        original_full_duration = self.duration.duration / self.contextual_reduction_factor 
        new_factor = self.unit_duration.duration * self.unit_duration_factor / original_full_duration  
        
        #  get the contextual reduction factor contribution the parent give to self.
        contrib = self.parent.contextual_reduction_factor if self.parent else 1
        orig_f = self.contextual_reduction_factor / contrib
        
        incremental_contextual_factor = new_factor / orig_f     # self.contextual_reduction_factor
        
        self.downward_refactor_layout(incremental_contextual_factor)            
   
    def __str__(self):
        base = 'Tuplet({0}x{1}Dur({2})Off({3})f={4})'.format(self.unit_duration, self.unit_duration_factor,
                                                             self.duration, self.relative_position,
                                                             self.contextual_reduction_factor)
        s = base + '[' + (']' if len(self.sub_notes) == 0 else '\n')
        for n in self.sub_notes:
            s += '  ' + str(n) + '\n'
        s += ']' if len(self.sub_notes) != 0 else ''
        return s
