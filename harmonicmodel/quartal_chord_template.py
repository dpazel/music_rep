"""

File: quartal_chord_template.py

Purpose: Class that defines a quartal chord in all its variations.

"""
from harmonicmodel.chord_template import ChordTemplate
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.interval import Interval, IntervalType
from harmonicmodel.quartal_chord import QuartalChord

import re
import logging


class QuartalChordType:
    """
    Enum class defining some significant quartal chord varieties.  There are 3 cases
    1) PerPer - Minor/Minor
    2) PerAug - Major/Minor
    3) AugPer - Minor/Major
    
    AugAug is not used as this amounts to root duplication.
    """
    PerPer, PerAug, AugPer = range(3)
    
    def __init__(self, ctype):
        self.value = ctype
        
    def __str__(self):
        if self.value == QuartalChordType.PerPer:
            return 'PerPer'
        if self.value == QuartalChordType.PerAug:
            return 'PerAug'
        if self.value == QuartalChordType.AugPer:
            return 'AugPer'
        
    @staticmethod
    def to_type(t_string):
        t = None
        if t_string == 'PerPer':
            t = QuartalChordType.PerPer
        if t_string == 'PerAug':
            t = QuartalChordType.PerAug
        if t_string == 'AugPer':
            t = QuartalChordType.AugPer
        return QuartalChordType(t) if t is not None else None
        
    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return self.__str__().__hash__()


class QuartalChordTemplate(ChordTemplate):
    """
    Template for quartal chords.  Quartal chords are based on incremental intervals of perfect and augmented intervals.
    This follows along the lines of Persechetti.  We do not used diminished 4th as they identify more with major 3rds.  
    
    We have a regular expression syntax to cover these cases that roughly goes:

    (Q|q)((I|II|...)|A-G)((PerPer|PerAug|AugPer| ...)|(m|M)+))?(@([1-9]([0-9]*)))?
    
    Examples:
      QII
      qCpapa
    """
    
    QUARTAL_CHORD_TYPE_MAP = {
        QuartalChordType.PerPer: [Interval(1, IntervalType.Perfect),
                                  Interval(4, IntervalType.Perfect),
                                  Interval(4, IntervalType.Perfect)],
        QuartalChordType.PerAug: [Interval(1, IntervalType.Perfect),
                                  Interval(4, IntervalType.Perfect),
                                  Interval(4, IntervalType.Augmented)],
        QuartalChordType.AugPer: [Interval(1, IntervalType.Perfect),
                                  Interval(4, IntervalType.Augmented),
                                  Interval(4, IntervalType.Perfect)],
    }

    GROUP_BASIS = 'Basis'
    GROUP_BASIS_TAG = '?P<' + GROUP_BASIS + '>'
    P1_BASIS = '(' + GROUP_BASIS_TAG + 'Q|q)'
    
    SCALE_DEGREE = 'III|II|IV|VII|VI|V|I|iii|ii|iv|vii|vi|v|i'
    GROUP_SCALE_DEGREE = 'ScaleDegree'
    GROUP_SCALE_DEGREE_TAG = '?P<' + GROUP_SCALE_DEGREE + '>'    
    
    GROUP_DIATONIC_TONE = 'DiatonicTone'
    GROUP_DIATONIC_TONE_NAME = '?P<' + GROUP_DIATONIC_TONE + '>' 
    ROOT = '((' + GROUP_DIATONIC_TONE_NAME + DiatonicTone.DIATONIC_PATTERN_STRING + ')|' + \
           '(' + GROUP_SCALE_DEGREE_TAG + SCALE_DEGREE + '))'

    CHORD_NAMES = 'PerPer|PerAug|AugPer'
    GROUP_CHORD = 'Chord'
    GROUP_CHORD_TAG = '?P<' + GROUP_CHORD + '>'  
    
    SECONDS = 'Seconds'
    SECONDS_SPECIFICATION_TAG = '?P<' + SECONDS + '>' 
    CHORDS = '((' + GROUP_CHORD_TAG + CHORD_NAMES + ')|(' + SECONDS_SPECIFICATION_TAG + '(p|P|a|A)+))?'
    
    INVERSION = '[1-9]([0-9]*)'
    GROUP_INVERSION = 'Inversion'
    GROUP_INVERSION_TAG = '?P<' + GROUP_INVERSION + '>'
    INVERSIONS = '(\@(' + GROUP_INVERSION_TAG + INVERSION + '))?'
    
    # full parse string and accompanying pattern for the secundal chord grammar.
    QUARTAL_PARSE_STRING = P1_BASIS + ROOT + CHORDS + INVERSIONS + '$'
    QUARTAL_PATTERN = re.compile(QUARTAL_PARSE_STRING)

    def __init__(self, diatonic_basis, scale_degree, chord_type, specified_fourths, inversion):
        """
        Constructor
        
        Args:
          diatonic_basis: DiatonicTone used as root of chord, e.g. C major chord, the C part
          scale_degree: int version of roman numeral
          chord_type: The chord type ala SecundalChordType
          specified_fourths: list of incremental fourth Interval's comprising the chord, e.g. [p, P, P]
                             usually used in lieu of, or addition to chord_type chord_type
          inversion: int for which of the chord tones (ordinal) serves as root [origin 1]
        """
        ChordTemplate.__init__(self)
        self.__diatonic_basis = diatonic_basis   # DiatonicTone
        
        self.__scale_degree = scale_degree   
        
        self.__chord_type = chord_type  
        self.__inversion = inversion    # which tone of n is the bass
        
        self.__base_intervals = []
        if chord_type:
            self.__base_intervals.extend(QuartalChordTemplate.QUARTAL_CHORD_TYPE_MAP[chord_type.value])
        self.__specified_fourths = specified_fourths
        if specified_fourths:
            intervals = list()
            intervals.append(Interval(1, IntervalType.Perfect))
            for ltr in specified_fourths:
                intervals.append(Interval(4, IntervalType.Perfect if ltr == 'P'or ltr == 'p'
                                                          else IntervalType.Augmented))
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
    def specified_fourths(self):
        return self.__specified_fourths
        
    def create_chord(self, diatonic_tonality):
        return QuartalChord(self, diatonic_tonality) 
    
    @staticmethod
    def get_chord_type(interval_list):
        for k, v in list(QuartalChordTemplate.QUARTAL_CHORD_TYPE_MAP.items()):
            if len(interval_list) == len(v):
                same = True
                for i in range(0, len(v)):
                    if not interval_list[i].is_same(v[i]):
                        same = False
                        break
                if same:
                    return QuartalChordType(k)
                
        # Build a M/m string
        t = ''
        for interval in interval_list[1:]:
            if interval.interval_type == IntervalType.Perfect:
                t += 'P'
            elif interval.interval_type == IntervalType.Augmented:
                t += 'A'
            else:
                raise Exception('Illegal interval type for quartal {0}'.format(interval))
        return t
        
    def __str__(self):
        return 'Q{0}{1}{2}{3}'.format(self.diatonic_basis.diatonic_symbol if self.diatonic_basis else
                                      (str(ChordTemplate.SCALE_DEGREE_REVERSE_MAP[self.scale_degree])),
                                      self.chord_type if self.chord_type else
                                      (self.specified_fourths if self.specified_fourths else ''),
                                      '@' + str(self.inversion) if self.inversion != 1 else '',
                                      ' --> ' + (' '.join(str(w) for w in self.base_intervals)),)
     
    @staticmethod   
    def parse(chord_string):
        """
        Parse an input string into a QuartalChordTemplate.
        
        Args:
          chord_string: string input representing chord
        Returns:
          QuartalChordTemplate       
        """
        if not chord_string:
            raise Exception('Unable to parse chord string to completion: {0}'.format(chord_string))
        m = QuartalChordTemplate.QUARTAL_PATTERN.match(chord_string)
        if not m:
            raise Exception('Unable to parse chord string to completion: {0}'.format(chord_string))
        
        scale_degree = m.group(QuartalChordTemplate.GROUP_SCALE_DEGREE)
        if scale_degree:
            scale_degree = ChordTemplate.SCALE_DEGREE_MAP[scale_degree]
        if m.group(QuartalChordTemplate.GROUP_DIATONIC_TONE) is not None:
            diatonic_basis = DiatonicTone(m.group(QuartalChordTemplate.GROUP_DIATONIC_TONE))
        else:
            diatonic_basis = None
        chord_name = m.group(QuartalChordTemplate.GROUP_CHORD)
        chord_type = None
        if chord_name:
            chord_type = QuartalChordType.to_type(chord_name)
      
        fourths = m.group(QuartalChordTemplate.SECONDS) 
        inversion_text = m.group(QuartalChordTemplate.GROUP_INVERSION)
        inversion = int(inversion_text) if inversion_text else 1
        
        logging.info('{0}, {1}, {2}, {3}'.format(diatonic_basis if scale_degree is None else str(scale_degree),
                                                 str(chord_type) if chord_type else '',
                                                 fourths if fourths else '',
                                                 inversion))
        return QuartalChordTemplate(diatonic_basis, scale_degree, chord_type, fourths, inversion)
