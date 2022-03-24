"""

File: tertian_chord_template.py

Purpose: Class that defines a tertian chord in all its variations.

"""
from harmonicmodel.chord_template import ChordTemplate
from tonalmodel.interval import Interval, IntervalType
from tonalmodel.diatonic_tone import DiatonicTone
from harmonicmodel.tertian_chord import TertianChord
import re
import logging


class TertianChordException(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)


class TertianChordType:
    """
    Enum class defining all the tertian chord varieties.
    """
    Maj6, Maj, Min6, Min, Dim, Aug, MajSus2, MajSus4, MajSus, Maj7, Maj7Sus4, Maj7Sus2, Maj7Sus, Min7, Dom7, Dom7Sus4, \
    Dom7Sus2, Dom7Sus, Dim7, HalfDim7, MinMaj7, AugMaj7, Aug7, DimMaj7, Dom7Flat5, Fr, Ger, It, N6 = range(29)

    def __init__(self, ctype):
        self.value = ctype

    def __str__(self):
        if self.value == TertianChordType.Maj:
            return 'Maj'
        if self.value == TertianChordType.Min:
            return 'Min'
        if self.value == TertianChordType.Dim:
            return 'Dim'
        if self.value == TertianChordType.Aug:
            return 'Aug'
        if self.value == TertianChordType.MajSus2:
            return 'MajSus2'
        if self.value == TertianChordType.MajSus4:
            return 'MajSus4'
        if self.value == TertianChordType.MajSus:
            return 'MajSus'
        if self.value == TertianChordType.Maj7:
            return 'Maj7'
        if self.value == TertianChordType.Maj7Sus4:
            return 'Maj7Sus4'
        if self.value == TertianChordType.Maj7Sus2:
            return 'Maj7Sus2'
        if self.value == TertianChordType.Maj7Sus:
            return 'Maj7Sus'
        if self.value == TertianChordType.Min7:
            return 'Min7'
        if self.value == TertianChordType.Dom7:
            return 'Dom7'
        if self.value == TertianChordType.Dom7Sus4:
            return 'Dom7Sus4'
        if self.value == TertianChordType.Dom7Sus2:
            return 'Dom7Sus2'
        if self.value == TertianChordType.Dom7Sus:
            return 'Dom7Sus'
        if self.value == TertianChordType.Dim7:
            return 'Dim7'
        if self.value == TertianChordType.HalfDim7:
            return 'HalfDim7'
        if self.value == TertianChordType.MinMaj7:
            return 'MinMaj7'
        if self.value == TertianChordType.AugMaj7:
            return 'AugMaj7'
        if self.value == TertianChordType.Aug7:
            return 'Aug7'
        if self.value == TertianChordType.DimMaj7:
            return 'DimMaj7'
        if self.value == TertianChordType.Dom7Flat5:
            return 'Dom7Flat5'
        if self.value == TertianChordType.Maj6:
            return 'Maj6'
        if self.value == TertianChordType.Min6:
            return 'Min6'
        if self.value == TertianChordType.Fr:
            return 'Fr'
        if self.value == TertianChordType.Ger:
            return 'Ger'
        if self.value == TertianChordType.It:
            return 'It'
        if self.value == TertianChordType.N6:
            return 'N6'

    @staticmethod
    def to_type(t_string):
        t = None
        if t_string == 'Maj':
            t = TertianChordType.Maj
        elif t_string == 'MajSus2':
            t = TertianChordType.MajSus2
        elif t_string == 'MajSus4':
            t = TertianChordType.MajSus4
        elif t_string == 'MajSus':
            t = TertianChordType.MajSus
        elif t_string == 'Min':
            t = TertianChordType.Min
        elif t_string == 'Dim':
            t = TertianChordType.Dim
        elif t_string == 'Aug':
            t = TertianChordType.Aug
        elif t_string == 'Maj7':
            t = TertianChordType.Maj7
        elif t_string == 'Maj7Sus2':
            t = TertianChordType.Maj7Sus2
        elif t_string == 'Maj7Sus4':
            t = TertianChordType.Maj7Sus4
        elif t_string == 'Maj7Sus':
            t = TertianChordType.Maj7Sus
        elif t_string == 'Min7':
            t = TertianChordType.Min7
        elif t_string == 'Dom7':
            t = TertianChordType.Dom7
        elif t_string == 'Dom7Sus2':
            t = TertianChordType.Dom7Sus2
        elif t_string == 'Dom7Sus4':
            t = TertianChordType.Dom7Sus4
        elif t_string == 'Dom7Sus':
            t = TertianChordType.Dom7Sus
        elif t_string == 'Dim7':
            t = TertianChordType.Dim7
        elif t_string == 'HalfDim7':
            t = TertianChordType.HalfDim7
        elif t_string == 'MinMaj7':
            t = TertianChordType.MinMaj7
        elif t_string == 'AugMaj7':
            t = TertianChordType.AugMaj7
        elif t_string == 'Aug7':
            t = TertianChordType.Aug7
        elif t_string == 'DimMaj7':
            t = TertianChordType.DimMaj7
        elif t_string == 'Dom7Flat5':
            t = TertianChordType.Dom7Flat5
        elif t_string == 'Maj6':
            t = TertianChordType.Maj6
        elif t_string == 'Min6':
            t = TertianChordType.Min6
        elif t_string == 'Fr':
            t = TertianChordType.Fr
        elif t_string == 'Ger':
            t = TertianChordType.Ger
        elif t_string == 'It':
            t = TertianChordType.It
        elif t_string == 'N6':
            t = TertianChordType.N6
        return TertianChordType(t) if t is not None else None

    def __eq__(self, y):
        return self.value == y.value

    def __hash__(self):
        return self.__str__().__hash__()


class TertianChordTemplate(ChordTemplate):
    """
    Template for tertian chords.  We have a regular expression syntax to cover these cases that roughly goes:

    (T|t)?((I|II|...)|A-G)(Maj|Min| ...)?(+?(b|#)?[2-15])*(@[1-7])?
    
    Examples:
      IIMaj7+b9@3
      CDom7
      TIVDim7Flat5#3      The third is sharped
      
    Note: The idea of modifiying scale degree ala:
              (+|-)?(I|II|...)
          was considered.  The notation traces back to -ii being used as a shorthand for Neopolian Six chords.
          The reference:
              https://en.wikipedia.org/wiki/Neapolitan_chord
          provides an interesting argument of using Phrygian scales to provide an underpinning for Neopolican.
          However, to take the notation to the next level, cases such as +iv and -vi need similar underpinning,
          which at this point cannot be found.  So we are not allowing this notation unless a solid theoretical
          solution appears.
    """

    TERTIAN_CHORD_TYPE_MAP = {
        TertianChordType.Maj: [Interval(1, IntervalType.Perfect),
                               Interval(3, IntervalType.Major),
                               Interval(5, IntervalType.Perfect)],
        TertianChordType.MajSus2: [Interval(1, IntervalType.Perfect),
                                   Interval(2, IntervalType.Major),
                                   Interval(5, IntervalType.Perfect)],
        TertianChordType.MajSus4: [Interval(1, IntervalType.Perfect),
                                   Interval(4, IntervalType.Perfect),
                                   Interval(5, IntervalType.Perfect)],
        TertianChordType.MajSus: [Interval(1, IntervalType.Perfect),
                                  Interval(4, IntervalType.Perfect),
                                  Interval(5, IntervalType.Perfect)],
        TertianChordType.Min: [Interval(1, IntervalType.Perfect),
                               Interval(3, IntervalType.Minor),
                               Interval(5, IntervalType.Perfect)],
        TertianChordType.Dim: [Interval(1, IntervalType.Perfect),
                               Interval(3, IntervalType.Minor),
                               Interval(5, IntervalType.Diminished)],
        TertianChordType.Aug: [Interval(1, IntervalType.Perfect),
                               Interval(3, IntervalType.Major),
                               Interval(5, IntervalType.Augmented)],
        TertianChordType.Maj7: [Interval(1, IntervalType.Perfect),
                                Interval(3, IntervalType.Major),
                                Interval(5, IntervalType.Perfect),
                                Interval(7, IntervalType.Major)],
        TertianChordType.Maj7Sus2: [Interval(1, IntervalType.Perfect),
                                    Interval(2, IntervalType.Major),
                                    Interval(5, IntervalType.Perfect),
                                    Interval(7, IntervalType.Major)],
        TertianChordType.Maj7Sus4: [Interval(1, IntervalType.Perfect),
                                    Interval(4, IntervalType.Perfect),
                                    Interval(5, IntervalType.Perfect),
                                    Interval(7, IntervalType.Major)],
        TertianChordType.Maj7Sus: [Interval(1, IntervalType.Perfect),
                                   Interval(4, IntervalType.Perfect),
                                   Interval(5, IntervalType.Perfect),
                                   Interval(7, IntervalType.Major)],
        TertianChordType.Min7: [Interval(1, IntervalType.Perfect),
                                Interval(3, IntervalType.Minor),
                                Interval(5, IntervalType.Perfect),
                                Interval(7, IntervalType.Minor)],
        TertianChordType.Dom7: [Interval(1, IntervalType.Perfect),
                                Interval(3, IntervalType.Major),
                                Interval(5, IntervalType.Perfect),
                                Interval(7, IntervalType.Minor)],
        TertianChordType.Dom7Sus2: [Interval(1, IntervalType.Perfect),
                                    Interval(2, IntervalType.Major),
                                    Interval(5, IntervalType.Perfect),
                                    Interval(7, IntervalType.Minor)],
        TertianChordType.Dom7Sus4: [Interval(1, IntervalType.Perfect),
                                    Interval(4, IntervalType.Perfect),
                                    Interval(5, IntervalType.Perfect),
                                    Interval(7, IntervalType.Minor)],
        TertianChordType.Dom7Sus: [Interval(1, IntervalType.Perfect),
                                   Interval(4, IntervalType.Perfect),
                                   Interval(5, IntervalType.Perfect),
                                   Interval(7, IntervalType.Minor)],
        TertianChordType.Dim7: [Interval(1, IntervalType.Perfect),
                                Interval(3, IntervalType.Minor),
                                Interval(5, IntervalType.Diminished),
                                Interval(7, IntervalType.Diminished)],
        TertianChordType.HalfDim7: [Interval(1, IntervalType.Perfect),
                                    Interval(3, IntervalType.Minor),
                                    Interval(5, IntervalType.Diminished),
                                    Interval(7, IntervalType.Minor)],
        TertianChordType.MinMaj7: [Interval(1, IntervalType.Perfect),
                                   Interval(3, IntervalType.Minor),
                                   Interval(5, IntervalType.Perfect),
                                   Interval(7, IntervalType.Major)],
        TertianChordType.AugMaj7: [Interval(1, IntervalType.Perfect),
                                   Interval(3, IntervalType.Major),
                                   Interval(5, IntervalType.Augmented),
                                   Interval(7, IntervalType.Major)],
        TertianChordType.Aug7: [Interval(1, IntervalType.Perfect),
                                Interval(3, IntervalType.Major),
                                Interval(5, IntervalType.Augmented),
                                Interval(7, IntervalType.Minor)],
        TertianChordType.DimMaj7: [Interval(1, IntervalType.Perfect),
                                   Interval(3, IntervalType.Minor),
                                   Interval(5, IntervalType.Diminished),
                                   Interval(7, IntervalType.Major)],
        TertianChordType.Dom7Flat5: [Interval(1, IntervalType.Perfect),
                                     Interval(3, IntervalType.Major),
                                     Interval(5, IntervalType.Diminished),
                                     Interval(7, IntervalType.Minor)],
        TertianChordType.Maj6: [Interval(1, IntervalType.Perfect),
                                Interval(3, IntervalType.Major),
                                Interval(5, IntervalType.Perfect),
                                Interval(6, IntervalType.Major)],
        TertianChordType.Min6: [Interval(1, IntervalType.Perfect),
                                Interval(3, IntervalType.Minor),
                                Interval(5, IntervalType.Perfect),
                                Interval(6, IntervalType.Major)],
        TertianChordType.Fr: [Interval(6, IntervalType.Augmented),
                              Interval(1, IntervalType.Perfect),
                              Interval(2, IntervalType.Major),
                              Interval(4, IntervalType.Augmented)],
        TertianChordType.Ger: [Interval(6, IntervalType.Augmented),
                               Interval(1, IntervalType.Perfect),
                               Interval(3, IntervalType.Minor),
                               Interval(4, IntervalType.Augmented)],
        TertianChordType.It: [Interval(6, IntervalType.Minor),
                              Interval(1, IntervalType.Perfect),
                              Interval(4, IntervalType.Augmented)],
        TertianChordType.N6: [Interval(6, IntervalType.Minor),
                              Interval(2, IntervalType.Minor),
                              Interval(4, IntervalType.Perfect)],
    }

    # Note that augmented 6th chords and the neopolitan have the sixth as the root.  This is the normal position.
    # And inversions specified alter that order.  So, root position would be inversion == 2.

    GROUP_BASIS = 'Basis'
    GROUP_BASIS_TAG = '?P<' + GROUP_BASIS + '>'
    P1_BASIS = '(' + GROUP_BASIS_TAG + 'T|t)?'

    SCALE_DEGREE = 'III|II|IV|VII|VI|V|I|iii|ii|iv|vii|vi|v|i'
    GROUP_SCALE_DEGREE = 'ScaleDegree'
    GROUP_SCALE_DEGREE_TAG = '?P<' + GROUP_SCALE_DEGREE + '>'

    GROUP_DIATONIC_TONE = 'DiatonicTone'
    GROUP_DIATONIC_TONE_NAME = '?P<' + GROUP_DIATONIC_TONE + '>'
    ROOT = '((' + GROUP_DIATONIC_TONE_NAME + DiatonicTone.DIATONIC_PATTERN_STRING + ')|' + \
           '(' + GROUP_SCALE_DEGREE_TAG + SCALE_DEGREE + '))'

    TENSION_RANGE = '(10|11|12|13|14|15|9|8|7|6|5|4|3|2|1)'
    TENSION = '((\\+)' + '(bb|b|##|#)?' + TENSION_RANGE + ')'
    GROUP_TENSIONS = 'Tensions'
    GROUP_TENSIONS_TAG = '?P<' + GROUP_TENSIONS + '>'
    TERTIAN_TENSIONS = '(' + GROUP_TENSIONS_TAG + TENSION + '*)'

    CHORD_NAMES = 'Maj7Sus4|Maj7Sus2|Maj7Sus|Maj7|MajSus4|MajSus2|MajSus|Maj6|Maj|Min7|MinMaj7|Min6|Min|DimMaj7|' \
                  'Dom7Flat5|Dim7|Dim|AugMaj7|Aug7|Aug|Dom7Sus4|Dom7Sus2|Dom7Sus|Dom7|HalfDim7|Fr|Ger|It|N6'

    GROUP_CHORD = 'Chord'
    GROUP_CHORD_TAG = '?P<' + GROUP_CHORD + '>'
    CHORDS = '(' + GROUP_CHORD_TAG + CHORD_NAMES + ')?'

    INVERSION = '[1-7]'
    GROUP_INVERSION = 'Inversion'
    GROUP_INVERSION_TAG = '?P<' + GROUP_INVERSION + '>'
    # INVERSIONS = '(\@(' + GROUP_INVERSION_TAG + INVERSION + '))?'

    INVERSION_TENSION = 'InvTension'
    INVERSION_TENSION_TAG = '?P<' + INVERSION_TENSION + '>'
    INVERSION_TENSION_STRUCT = '\\(' + '(bb|b|##|#)?' + TENSION_RANGE + '\\)'
    INVERSION_TENSION_PATTERN = '(' + INVERSION_TENSION_TAG + INVERSION_TENSION_STRUCT + ')'
    INVERSIONS = '(\\@(' + GROUP_INVERSION_TAG + INVERSION + '|' + INVERSION_TENSION_PATTERN + '))?'

    # full parse string and accompanying pattern for the tertian chord grammar.
    TERTIAN_PARSE_STRING = P1_BASIS + ROOT + CHORDS + TERTIAN_TENSIONS + INVERSIONS + '$'
    TERTIAN_PATTERN = re.compile(TERTIAN_PARSE_STRING)

    TENSION_PATTERN = re.compile(TENSION)
    INVERSE_TENSION_PATTERN = re.compile(INVERSION_TENSION_STRUCT)

    def __init__(self, diatonic_basis, scale_degree, chord_type, tension_intervals, inversion, inversion_interval=None):
        """
        Constructor
        
        Args:
          diatonic_basis: DiatonicTone used as root of chord, e.g. C major chord, the C part
          scale_degree: int version of roman numeral
          chord_type: The chord type ala TertianChordType
          tension_intervals: list of Interval's comprising the tensions
          inversion: int for which of the chord tones (ordinal) serves as root [origin 1]
          inversion_interval: if specified, indicates which interval should be the base.
          (both this in interval cannot be non-null.)
        """
        ChordTemplate.__init__(self)
        self.__diatonic_basis = diatonic_basis  # DiatonicTone

        self.__scale_degree = scale_degree

        self.__chord_type = chord_type
        self.__tension_intervals = tension_intervals  # list of [number, augmentation] representing intervals
        self.__inversion = inversion  # which tone of n is the bass
        self.__inversion_interval = inversion_interval

        self.__base_intervals = []
        if chord_type:
            self.__base_intervals.extend(TertianChordTemplate.TERTIAN_CHORD_TYPE_MAP[self.chord_type.value])

        # Remove duplicate tensions
        seen = set()
        seen_add = seen.add
        deduped_tension_intervals = [tension for tension in self.tension_intervals
                                     if not (tension.semitones() in seen or seen_add(tension.semitones()))]
        self.__tension_intervals = deduped_tension_intervals

        # Inversion check - only if chord type was given, not for cases like II
        if self.chord_type and (self.inversion is not None) and \
                self.inversion > len(self.base_intervals) + len(self.tension_intervals):
            raise Exception('Illegal inversion {0} for {1}'.format(self.inversion, self.__str__()))

        if self.inversion_interval is not None and \
                self.inversion_interval not in self.base_intervals and \
                self.inversion_interval not in self.tension_intervals:
            raise Exception('Illegal inversion_interval {0}'.format(self.inversion_interval))

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
    def tension_intervals(self):
        return self.__tension_intervals

    @property
    def inversion(self):
        return self.__inversion

    @property
    def inversion_interval(self):
        return self.__inversion_interval

    @staticmethod
    def get_chord_type(interval_list):
        for k, v in list(TertianChordTemplate.TERTIAN_CHORD_TYPE_MAP.items()):
            if len(interval_list) == len(v):
                same = True
                for i in range(0, len(v)):
                    if not interval_list[i].is_same(v[i]):
                        same = False
                        break
                if same:
                    return TertianChordType(k)
        return None

    @staticmethod
    def get_triad(diatonic_tonality, scale_degree):
        return TertianChordTemplate.parse('t{0}'.format(
            ChordTemplate.SCALE_DEGREE_REVERSE_MAP[scale_degree])).create_chord(diatonic_tonality)

    def create_chord(self, diatonic_tonality=None):
        return TertianChord(self, diatonic_tonality)

    def __str__(self):
        inv = ''
        if self.inversion is not None and self.inversion != 1:
            inv = '@' + str(self.inversion)
        elif self.inversion_interval is not None:
            inv = '@(' + str(self.inversion_interval) + ')'
        return 'T{0}{1}{2}{3}'.format(
            self.diatonic_basis.diatonic_symbol if self.diatonic_basis else
            (str(ChordTemplate.SCALE_DEGREE_REVERSE_MAP[self.scale_degree])),
            self.chord_type if self.chord_type else '',
            ' '.join(str(w) for w in self.tension_intervals),
            inv)

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
            raise TertianChordException('Unable to parse chord string to completion: {0}'.format(chord_string))
        m = TertianChordTemplate.TERTIAN_PATTERN.match(chord_string)
        if not m:
            raise TertianChordException('Unable to parse chord string to completion: {0}'.format(chord_string))

        scale_degree = m.group(TertianChordTemplate.GROUP_SCALE_DEGREE)
        if scale_degree:
            scale_degree = ChordTemplate.SCALE_DEGREE_MAP[scale_degree]
        if m.group(TertianChordTemplate.GROUP_DIATONIC_TONE) is not None:
            diatonic_basis = DiatonicTone(m.group(TertianChordTemplate.GROUP_DIATONIC_TONE))
        else:
            diatonic_basis = None
        chord_name = m.group(TertianChordTemplate.GROUP_CHORD)
        chord_type = None
        if chord_name:
            chord_type = TertianChordType.to_type(chord_name)
        inversion_text = m.group(TertianChordTemplate.GROUP_INVERSION)
        inversion_tension = m.group(TertianChordTemplate.INVERSION_TENSION)
        inversion_interval = None
        inversion = None
        if inversion_tension:
            tensions_parse = TertianChordTemplate.INVERSE_TENSION_PATTERN.findall(inversion_tension)
            for tension in tensions_parse:  # should only be 1
                aug = DiatonicTone.AUGMENTATION_OFFSET_MAPPING[tension[0]]
                interval_type = Interval.available_types(int(tension[1]))[aug]
                inversion_interval = Interval(int(tension[1]), interval_type)
                logging.info('inversion_interval = {0}'.format(str(inversion_interval)))
        elif inversion_text:
            inversion = int(inversion_text)
        else:
            inversion = 1

        tensions = []
        if m.group(TertianChordTemplate.GROUP_TENSIONS):
            tensions_parse = TertianChordTemplate.TENSION_PATTERN.findall(m.group(TertianChordTemplate.GROUP_TENSIONS))
            for tension in tensions_parse:
                aug = DiatonicTone.AUGMENTATION_OFFSET_MAPPING[tension[2]]
                if aug not in Interval.available_types(int(tension[3])):
                    raise TertianChordException('Invalid interval specification for tension \'{0}\''.format(tension[0]))
                interval_type = Interval.available_types(int(tension[3]))[aug]
                interval = Interval(int(tension[3]), interval_type)
                tensions.append(interval)

        # logging.info('{0}, {1}, {2}, {3}'.format(diatonic_basis if scale_degree is None else str(scale_degree),
        #                                         str(chord_type) if chord_type else '',
        #                                         ' '.join(str(x) for x in tensions) if tensions else '',
        #                                        inversion if inversion else ''))
        return TertianChordTemplate(diatonic_basis, scale_degree, chord_type, tensions, inversion, inversion_interval)
