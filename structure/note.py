"""

File: note.py

Purpose: Defines the basic Note class that holds a pitch, duration, dots, tie information.

"""

from structure.abstract_note import AbstractNote

from timemodel.duration import Duration


class Note(AbstractNote):
    """
    Class representation for a musical note.
    """

    STANDARD_NOTES = {'W': Duration(1),
                      'H': Duration(1, 2),
                      'Q': Duration(1, 4),
                      'E': Duration(1, 8),
                      'S': Duration(1, 16),
                      'T': Duration(1, 32),
                      'X': Duration(1, 64),
                      }

    def __init__(self, diatonic_pitch,  base_duration, num_dots=0):
        """
        Constructor.
        
        Args
          diatontic_pitch: ref. class DiatonicPitch.
          base_duration: either a Duration, or key in STANDARD_NOTES (upper or lower case).
          num_dots: number of duration extension dots.
        """
        AbstractNote.__init__(self)
        
        self.__diatonic_pitch = diatonic_pitch
        self.__num_dots = num_dots
        if type(base_duration) == Duration:
            self.__base_duration = base_duration
        elif isinstance(base_duration, str):
            if base_duration.upper() in Note.STANDARD_NOTES.keys():
                self.__base_duration = Note.STANDARD_NOTES[base_duration.upper()]
            else:
                raise Exception('Base duration can only be a Duration or string in key set [w, h, q, e, s, t. x]')
        self.__duration = self.base_duration.apply_dots(num_dots)
        
        self.__tied_to = None
        self.__tied_from = None
        
    @property
    def diatonic_pitch(self):
        return self.__diatonic_pitch

    @diatonic_pitch.setter
    def diatonic_pitch(self, new_pitch):
        self.__diatonic_pitch = new_pitch
    
    @property
    def duration(self):
        return self.__duration
    
    @property 
    def base_duration(self):
        return self.__base_duration
    
    @property
    def num_dots(self):
        return self.__num_dots
    
    @property
    def is_tied_to(self):
        return self.__tied_to is not None
    
    @property
    def is_tied_from(self):
        return self.__tied_from is not None
    
    @property
    def tied_to(self):
        return self.__tied_to
    
    @property
    def tied_from(self):
        return self.__tied_from
    
    @property
    def is_rest(self):
        return self.diatonic_pitch is None
    
    def get_all_notes(self): 
        return [self]
    
    def tie(self):
        """
        Tie this note to the next note.
        """
        original_parent = self.get_original_parent()
        if original_parent is None:
            raise Exception('Cannot tie note that has no parent')
        note = self.next_note()
        if note is None:
            raise Exception('No next note to tie to.')
        
        # notes must have the same pitch
        if note.diatonic_pitch != self.diatonic_pitch:
            raise Exception(
                'Tied notes require to have same pitch {0} != {1}'.format(self.diatonic_pitch, note.diatonic_pitch))
        
        self.__tied_to = note
        note.__tied_from = self
        
    def untie(self):
        if not self.is_tied_to:
            return
        
        self.__tied_to.__tied_from = None
        self.__tied_to = None
    
    def next_note(self):
        """
        Determine the successor Note within the context of the note structure parentage.
        
        Returns:
          The successor Note, or None if there is none, e.g. this is the last note.
        """
        child = self
        p = child.parent
        
        while True:
            if p is None:
                break
            next_str = p.get_next_child(child)
            if next_str is not None:
                if isinstance(next_str, Note):
                    return next_str
                else:
                    return next_str.get_first_note()
            else:
                child = p
                p = p.parent
        # At this point, we are the last note in the structure - there is no next
        return None
      
    def prior_note(self):
        """
        Determine the Note prior to this one within the context of the note structure parentage.
        
        Returns:
          The prior Note, or None is there is none, e.g. this is the first note.
        """
        child = self
        p = child.parent
        
        while True:
            if p is None:
                break
            next_str = p.get_prior_child(child)
            if next_str is not None:
                if isinstance(next_str, Note):
                    return next_str
                else:
                    return next_str.get_last_note()
            else:
                child = p
                p = p.parent
        # At this point, we are the last note in the structure - there is no next
        return None        
           
    def apply_factor(self, factor):
        self.__base_duration *= factor
        self.__duration *= factor
        self.relative_position *= factor
        self.contextual_reduction_factor *= factor
        
    def reverse(self):
        return self
    
    def __str__(self):
        dot_string = str(self.base_duration) + self.num_dots * '@'        
        return '[{0}<{1}>-({2}){3}] off={4} f={5}'.format(
            self.diatonic_pitch if self.diatonic_pitch is not None else 'R', dot_string, self.duration,
            'T' if self.is_tied_to else '', self.relative_position, self.contextual_reduction_factor)
