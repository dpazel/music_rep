"""

File: secondary_chord_template.py

Purpose: Represent the definition of a secondary chord.

"""
from harmonicmodel.chord_template import ChordTemplate
from tonalmodel.diatonic_modality import DiatonicModality
from harmonicmodel.secondary_chord import SecondaryChord
from tonalmodel.modality import ModalityType

import re
import logging


class SecondaryChordTemplate(ChordTemplate):
    """
    Class representing the definition of a secondary chord.
    """
    
    SCALE_DEGREE = 'III|II|IV|VII|VI|V|I|iii|ii|iv|vii|vi|v|i'
    SCALE_DEGREE_NAME = 'ScaleDegree'
    SCALE_DEGREE_TAG = '?P<' + SCALE_DEGREE_NAME + '>' 
    
    INITIAL_CHORD_TEXT_NAME = 'InitialChordText'
    INITIAL_CHORD_TEXT_TAG = '?P<' + INITIAL_CHORD_TEXT_NAME + '>'
    INITIAL_CHORD = '(' + INITIAL_CHORD_TEXT_TAG + '[^/]*)'
    
    DIATONIC_MODALITIES = '|'.join(DiatonicModality.diatonic_modality_types_as_string_array())
    DIATONIC_MODALITIES_NAME = 'DiatonicModality'
    DIATONIC_MODALITIES_TAG = '?P<' + DIATONIC_MODALITIES_NAME + '>'
    DIATONIC_MODALITY = '(' + DIATONIC_MODALITIES_TAG + DIATONIC_MODALITIES + ')'
    
    SECONDARY_BASIS = '(' + SCALE_DEGREE_TAG + SCALE_DEGREE + ')' + '(\[' + DIATONIC_MODALITY + '\])?'
    
    # full parse string and accompanying pattern for the secondary chord grammar.
    SECONDARY_CHORD_PARSE_STRING = INITIAL_CHORD + '/' + SECONDARY_BASIS + '$'
    SECONDARY_CHORD_PATTERN = re.compile(SECONDARY_CHORD_PARSE_STRING)

    def __init__(self, principal_chord_template, secondary_scale_degree, secondary_modality):
        """
        Constructor.
        
        Args:
        principal_chord_template: ChordTemplate for the numerator. 
        secondary_scale_degree: (int) which scale degree 1 --> 6.
        secondary_modality: Modality for the denominator if specified (None if not specified).
        """
        ChordTemplate.__init__(self)

        self.__principal_chord_template = principal_chord_template
        self.__secondary_scale_degree = secondary_scale_degree
        self.__secondary_modality = secondary_modality 
        
    def __str__(self):
        return '{0}/{1}-{2}'.format(str(self.principal_chord_template),
                                    ChordTemplate.SCALE_DEGREE_REVERSE_MAP[self.secondary_scale_degree],
                                    self.secondary_modality)
        
    @property
    def principal_chord_template(self):
        return self.__principal_chord_template
    
    @property
    def secondary_scale_degree(self):
        return self.__secondary_scale_degree
    
    @property
    def secondary_modality(self):
        return self.__secondary_modality
                
    def create_chord(self, diatonic_tonality):
        return SecondaryChord(self, diatonic_tonality)
        
    @staticmethod   
    def parse(chord_string):
        """
        Parse an input string into a TertialChordTemplate.
        
        Args:
          chord_string: string input representing chord
        Returns:
          TertianChordTemplate       
        """
        if not chord_string:
            raise Exception('Unable to parse chord string to completion: {0}'.format(chord_string))
        m = SecondaryChordTemplate.SECONDARY_CHORD_PATTERN.match(chord_string)
        if not m:
            raise Exception('Unable to parse chord string to completion: {0}'.format(chord_string))  
        
        principal_chord_text = m.group(SecondaryChordTemplate.INITIAL_CHORD_TEXT_NAME)     
        
        secondary_scale_degree_text = m.group(SecondaryChordTemplate.SCALE_DEGREE_NAME)
        secondary_scale_degree = ChordTemplate.SCALE_DEGREE_MAP[secondary_scale_degree_text]
        
        secondary_modality_text = m.group(SecondaryChordTemplate.DIATONIC_MODALITIES_NAME)
        secondary_modality = ModalityType.to_type(secondary_modality_text) if secondary_modality_text else None
        
        principal_chord_template = ChordTemplate.generic_chord_template_parse(principal_chord_text)
        if not principal_chord_template:
            raise Exception('Unable to parse principle chord in secondary template: {0}'.format(principal_chord_text))
            
        logging.info('{0}, {1}, {2}, {3}'.format(principal_chord_text,
                                                 str(principal_chord_template),
                                                 secondary_scale_degree,
                                                 str(secondary_modality) if secondary_modality else ''))
        
        return SecondaryChordTemplate(principal_chord_template, secondary_scale_degree, secondary_modality)          