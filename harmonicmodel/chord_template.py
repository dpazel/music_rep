"""

File: chord_template.py

Purpose: Defines an abstract class to represent a kind of chord.

"""
from abc import ABCMeta, abstractmethod


class ChordTemplate(object):
    """
    This is a base class for all chord definitions.
    """
    
    SCALE_DEGREE_MAP = {
        'I': 1, 'i': 1,
        'II': 2, 'ii': 2,
        'III': 3, 'iii': 3,
        'IV': 4, 'iv': 4,
        'V': 5, 'v': 5,
        'VI': 6, 'vi': 6,
        'VII': 7, 'vii': 7,
        'VIII': 8, 'viii': 8,
        'IX': 9, 'ix': 9,
        'X': 10, 'x': 10,
        'XI': 11, 'xi': 11,
        'XII': 12, 'xii': 12,
    }
    
    SCALE_DEGREE_REVERSE_MAP = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'
                                }
    __metaclass__ = ABCMeta
    
    def __init__(self):
        """
        Constructor
        """

    @abstractmethod
    def create_chord(self, diatonic_modality):
        raise NotImplementedError('users must define create_chord to use this base class')   
    
    @staticmethod
    def generic_chord_template_parse(chord_txt):
        """
        Generic text parse into chord template.
        
        Args:
          chord_txt: String
        Returns:
          ChordTemplate or None if fails.
        """

        #  Try parsing chord text through known chord templates.
        #  If all fail, just return None.
        from harmonicmodel.secondary_chord_template import SecondaryChordTemplate
        try:
            chord_template = SecondaryChordTemplate.parse(chord_txt)
            return chord_template
        except Exception as e:
            pass
        from harmonicmodel.tertian_chord_template import TertianChordTemplate
        try:
            chord_template = TertianChordTemplate.parse(chord_txt)
            return chord_template
        except Exception:
            pass
        from harmonicmodel.secundal_chord_template import SecundalChordTemplate
        try:
            chord_template = SecundalChordTemplate.parse(chord_txt)
            return chord_template
        except Exception:
            pass
        from harmonicmodel.quartal_chord_template import QuartalChordTemplate
        try:
            chord_template = QuartalChordTemplate.parse(chord_txt)
            return chord_template
        except Exception:
            return None     