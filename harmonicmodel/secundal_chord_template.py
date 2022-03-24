"""

File: secundal_chord_template.py

Purpose: Class that defines a secundal chord in all its variations.

"""
from harmonicmodel.chord_template import ChordTemplate
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.interval import Interval, IntervalType
from harmonicmodel.secundal_chord import SecundalChord

import re
import logging


class SecundalChordException(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)


class SecundalChordType:
    """
    Enum class defining some significant secundal chord varieties.  There are 4 cases
    1) MinMin - Minor/Minor
    2) MajMin - Major/Minor
    3) MinMaj - Minor/Major
    4) MajMaj - Major/Major
    """
    MinMin, MajMin, MinMaj, MajMaj = range(4)
    
    def __init__(self, ctype):
        self.value = ctype
        
    def __str__(self):
        if self.value == SecundalChordType.MinMin:
            return 'MinMin'
        if self.value == SecundalChordType.MajMin:
            return 'MajMin'
        if self.value == SecundalChordType.MinMaj:
            return 'MinMaj'
        if self.value == SecundalChordType.MajMaj:
            return 'MajMaj'
        
    @staticmethod
    def to_type(t_string):
        t = None
        if t_string == 'MinMin':
            t = SecundalChordType.MinMin
        if t_string == 'MajMin':
            t = SecundalChordType.MajMin
        if t_string == 'MinMaj':
            t = SecundalChordType.MinMaj
        if t_string == 'MajMaj':
            t = SecundalChordType.MajMaj
        return SecundalChordType(t) if t is not None else None
        
    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return self.__str__().__hash__()
    

class SecundalChordTemplate(ChordTemplate):
    """
    Template for secundal chords.  Secundal chords are based on incremental intervals of major and minor 2nd intervals.  
    
    We have a regular expression syntax to cover these cases that roughly goes:

    (S|s)((I|II|...)|A-G)((MinMin|MinMaj|MajMin|MajMaj| ...)|(m|M)+))?(@([1-9]([0-9]*)))?
    
    Examples:
      sII
      sCMmM
      
    Note: Along the lines of tertian, the idea of modifiying scale degree ala:
              (+|-)?(I|II|...)
          was considered.  The notation traces back to -ii being used as a shorthand for Neopolian Six chords.
          The reference:
              https://en.wikipedia.org/wiki/Neapolitan_chord
          provides an interesting argument of using Phrygian scales to provide an underpinning for Neopolican.
          However, to take the notation to the next level, cases such as +iv and -vi need similar underpinning,
          which at this point cannot be found.  So we are not allowing this notation unless a solid theoretical
          solution appears.
          
    """
    
    SECUNDAL_CHORD_TYPE_MAP = {
        SecundalChordType.MinMin: [Interval(1, IntervalType.Perfect),
                                   Interval(2, IntervalType.Minor),
                                   Interval(2, IntervalType.Minor)],
        SecundalChordType.MajMin: [Interval(1, IntervalType.Perfect),
                                   Interval(2, IntervalType.Major),
                                   Interval(2, IntervalType.Minor)],
        SecundalChordType.MinMaj: [Interval(1, IntervalType.Perfect),
                                   Interval(2, IntervalType.Minor),
                                   Interval(2, IntervalType.Major)],
        SecundalChordType.MajMaj: [Interval(1, IntervalType.Perfect),
                                   Interval(2, IntervalType.Major),
                                   Interval(2, IntervalType.Major)],
    }

    GROUP_BASIS = 'Basis'
    GROUP_BASIS_TAG = '?P<' + GROUP_BASIS + '>'
    P1_BASIS = '(' + GROUP_BASIS_TAG + 'S|s)?'
    
    SCALE_DEGREE = 'III|II|IV|VII|VI|V|I|iii|ii|iv|vii|vi|v|i'
    GROUP_SCALE_DEGREE = 'ScaleDegree'
    GROUP_SCALE_DEGREE_TAG = '?P<' + GROUP_SCALE_DEGREE + '>'    
    
    GROUP_DIATONIC_TONE = 'DiatonicTone'
    GROUP_DIATONIC_TONE_NAME = '?P<' + GROUP_DIATONIC_TONE + '>' 
    ROOT = '((' + GROUP_DIATONIC_TONE_NAME + DiatonicTone.DIATONIC_PATTERN_STRING + ')|' + \
           '(' + GROUP_SCALE_DEGREE_TAG + SCALE_DEGREE + '))'

    CHORD_NAMES = 'MinMin|MinMaj|MajMin|MajMaj'
    GROUP_CHORD = 'Chord'
    GROUP_CHORD_TAG = '?P<' + GROUP_CHORD + '>'  
    
    SECONDS = 'Seconds'
    SECONDS_SPECIFICATION_TAG = '?P<' + SECONDS + '>' 
    CHORDS = '((' + GROUP_CHORD_TAG + CHORD_NAMES + ')|(' + SECONDS_SPECIFICATION_TAG + '(m|M)+))?'
    
    INVERSION = '[1-9]([0-9]*)'
    GROUP_INVERSION = 'Inversion'
    GROUP_INVERSION_TAG = '?P<' + GROUP_INVERSION + '>'
    INVERSIONS = '(\\@(' + GROUP_INVERSION_TAG + INVERSION + '))?'
    
    # full parse string and accompanying pattern for the secundal chord grammar.
    SECUNDAL_PARSE_STRING = P1_BASIS + ROOT + CHORDS + INVERSIONS + '$'
    SECUNDAL_PATTERN = re.compile(SECUNDAL_PARSE_STRING)  

    def __init__(self, diatonic_basis, scale_degree, chord_type, specified_seconds, inversion):
        """
        Constructor
        
        Args:
          diatonic_basis: DiatonicTone used as root of chord, e.g. C major chord, the C part
          scale_degree: int version of roman numeral
          chord_type: The chord type ala SecundalChordType
          specified_seconds: list of Interval's secondary notes
          inversion: int for which of the chord tones (ordinal) serves as root [origin 1]
        """
        ChordTemplate.__init__(self)
        self.__diatonic_basis = diatonic_basis   # DiatonicTone
        
        self.__scale_degree = scale_degree   
        
        self.__chord_type = chord_type  
        self.__inversion = inversion    # which tone of n is the bass
        
        self.__base_intervals = list()
        if chord_type:
            self.__base_intervals.extend(SecundalChordTemplate.SECUNDAL_CHORD_TYPE_MAP[chord_type.value])
        self.__specified_seconds = specified_seconds
        if specified_seconds:
            intervals = list()
            intervals.append(Interval(1, IntervalType.Perfect))
            for ltr in specified_seconds:
                intervals.append(Interval(2, IntervalType.Major if ltr == 'M' else IntervalType.Minor))
            self.__base_intervals.extend(intervals)
                 
        # Inversion check - only if chord type was given, not for cases like II
        if self.chord_type and self.inversion > len(self.base_intervals):
            raise Exception('Illegal inversion {0} for {1}'.format(self.inversion, self.__str__()))
        
    @property
    def diatonic_basis(self):
        return self.__diatonic_basis
     
    @property   
    def scale_degree(self):
        return self.__scale_degree
    
    @property
    def chord_type(self):
        return self.__chord_type
    
    @property
    def base_intervals(self):
        return self.__base_intervals
    
    @property
    def inversion(self):
        return self.__inversion
    
    @property
    def specified_seconds(self):
        return self.__specified_seconds
        
    def create_chord(self, diatonic_tonality=None):
        return SecundalChord(self, diatonic_tonality) 
    
    @staticmethod
    def get_chord_type(interval_list):
        for k, v in list(SecundalChordTemplate.SECUNDAL_CHORD_TYPE_MAP.items()):
            if len(interval_list) == len(v):
                same = True
                for i in range(0, len(v)):
                    if not interval_list[i].is_same(v[i]):
                        same = False
                        break
                if same:
                    return SecundalChordType(k)
                
        # Build a M/m string
        t = ''
        for interval in interval_list[1:]:
            if interval.interval_type == IntervalType.Major:
                t += 'M'
            elif interval.interval_type == IntervalType.Minor:
                t += 'm'
            else:
                raise Exception('Illegal interval type for secundal {0}'.format(interval))
        return t
        
    def __str__(self):
        return 'S{0}{1}{2}{3}'.format(
            self.diatonic_basis.diatonic_symbol if self.diatonic_basis else
            (str(ChordTemplate.SCALE_DEGREE_REVERSE_MAP[self.scale_degree])),
            self.chord_type if self.chord_type else (self.specified_seconds if self.specified_seconds else ''),
            '@' + str(self.inversion) if self.inversion != 1 else '',
            ' --> ' + (' '.join(str(w) for w in self.base_intervals)),)
        
    @staticmethod   
    def parse(chord_string):
        """
        Parse an input string into a SecundalChordTemplate.
        
        Args:
          chord_string: string input representing chord
        Returns:
          SecundalChordTemplate       
        """
        if not chord_string:
            raise SecundalChordException('Unable to parse chord string to completion: {0}'.format(chord_string))
        m = SecundalChordTemplate.SECUNDAL_PATTERN.match(chord_string)
        if not m:
            raise SecundalChordException('Unable to parse chord string to completion: {0}'.format(chord_string))
        
        scale_degree = m.group(SecundalChordTemplate.GROUP_SCALE_DEGREE)
        if scale_degree:
            scale_degree = ChordTemplate.SCALE_DEGREE_MAP[scale_degree]
        if m.group(SecundalChordTemplate.GROUP_DIATONIC_TONE) is not None:
            diatonic_basis = DiatonicTone(m.group(SecundalChordTemplate.GROUP_DIATONIC_TONE))
        else:
            diatonic_basis = None
        chord_name = m.group(SecundalChordTemplate.GROUP_CHORD)
        chord_type = None
        if chord_name:
            chord_type = SecundalChordType.to_type(chord_name)
      
        seconds = m.group(SecundalChordTemplate.SECONDS) 
        inversion_text = m.group(SecundalChordTemplate.GROUP_INVERSION)
        inversion = int(inversion_text) if inversion_text else 1
        
        logging.info('{0}, {1}, {2}, {3}'.format(diatonic_basis if scale_degree is None else str(scale_degree),
                                                 str(chord_type) if chord_type else '',
                                                 seconds if seconds else '',
                                                 inversion))
        return SecundalChordTemplate(diatonic_basis, scale_degree, chord_type, seconds, inversion)
