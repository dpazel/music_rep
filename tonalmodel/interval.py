"""
File: interval.py

Purpose: Defines Interval and IntervalType classes.

"""
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.diatonic_foundation import DiatonicFoundation

import re
from enum import Enum


class IntervalType(Enum):
    """
    Enum class for the quality of musical intervals.
    """
    Major = 1
    Minor = 2
    Diminished = 3
    Augmented = 4
    Perfect = 5

    @staticmethod
    def short_notation(t):
        if t == IntervalType.Major:
            return "M"
        elif t == IntervalType.Minor:
            return "m"
        elif t == IntervalType.Diminished:
            return "d"
        elif t == IntervalType.Augmented:
            return "A"
        elif t == IntervalType.Perfect:
            return "P"
        raise Exception('Invalid interval key {0}.'.format(t))

    def __str__(self):
        return self.name


class Interval(object):
    """
    Class that encapsulates the notions of a musical interval.
    An interval is a diatonic measure of distance between two diatonic pitches.  It is qualified by two attributes
    1) The number of letter steps between the two pitches
    2) A qualitative characterization of the sound of the distance, as given by IntervalType
    
    We strictly enforce that the starting pitch must precede the end pitch. 
    """
    
    # mapping (diatonic-distance, semitone distance) --> IntervalType
    #   Note:  We are excluding 'diminished unison', as it causes consistency issues, and is controversial.
    #          Although 'augmented octave' is valid in itself, due to the above, it's inversion is illegal.
    INTERVAL_MAP = {
        (0, -1): IntervalType.Diminished,
        (0, 0): IntervalType.Perfect,
        (0, 1): IntervalType.Augmented,
        (1, 0): IntervalType.Diminished,
        (1, 1): IntervalType.Minor,
        (1, 2): IntervalType.Major,
        (1, 3): IntervalType.Augmented,
        (2, 2): IntervalType.Diminished,
        (2, 3): IntervalType.Minor,
        (2, 4): IntervalType.Major,
        (2, 5): IntervalType.Augmented,
        (3, 4): IntervalType.Diminished,
        (3, 5): IntervalType.Perfect,
        (3, 6): IntervalType.Augmented,
        (4, 6): IntervalType.Diminished,
        (4, 7): IntervalType.Perfect,
        (4, 8): IntervalType.Augmented,
        (5, 7): IntervalType.Diminished,
        (5, 8): IntervalType.Minor,
        (5, 9): IntervalType.Major,
        (5, 10): IntervalType.Augmented,
        (6, 9):  IntervalType.Diminished,
        (6, 10): IntervalType.Minor,
        (6, 11): IntervalType.Major,
        (6, 12): IntervalType.Augmented,
        (7, 11): IntervalType.Diminished,
        (7, 12): IntervalType.Perfect,
        (7, 13): IntervalType.Augmented,
    }
    
    INVERSE_INTERVAL_MAP = {(v, k[0]): k[1] for k, v in INTERVAL_MAP.items()}
    
    INTERVAL_AVAILABLE_TYPES = {
            1: {-1: IntervalType.Diminished, 0: IntervalType.Perfect, 1: IntervalType.Augmented},
            2: {-2: IntervalType.Diminished, -1: IntervalType.Minor, 0: IntervalType.Major, 1: IntervalType.Augmented},
            3: {-2: IntervalType.Diminished, -1: IntervalType.Minor, 0: IntervalType.Major, 1: IntervalType.Augmented},
            4: {-1: IntervalType.Diminished, 0: IntervalType.Perfect, 1: IntervalType.Augmented},
            5: {-1: IntervalType.Diminished, 0: IntervalType.Perfect, 1: IntervalType.Augmented},
            6: {-2: IntervalType.Diminished, -1: IntervalType.Minor, 0: IntervalType.Major, 1: IntervalType.Augmented},
            7: {-2: IntervalType.Diminished, -1: IntervalType.Minor, 0: IntervalType.Major, 1: IntervalType.Augmented},
    }
    
    VALID_INTERVALS = {
        (0, IntervalType.Diminished),
        (0, IntervalType.Perfect),
        (0, IntervalType.Augmented),
        (1, IntervalType.Diminished),
        (1, IntervalType.Minor),
        (1, IntervalType.Major),
        (1, IntervalType.Augmented),
        (2, IntervalType.Diminished),
        (2, IntervalType.Minor),
        (2, IntervalType.Major),
        (2, IntervalType.Augmented),
        (3, IntervalType.Diminished),
        (3, IntervalType.Perfect),
        (3, IntervalType.Augmented),
        (4, IntervalType.Diminished),
        (4, IntervalType.Perfect),
        (4, IntervalType.Augmented),
        (5, IntervalType.Diminished),
        (5, IntervalType.Minor),
        (5, IntervalType.Major),
        (5, IntervalType.Augmented),
        (6, IntervalType.Diminished),
        (6, IntervalType.Minor),
        (6, IntervalType.Major),
        (6, IntervalType.Augmented),
        (7, IntervalType.Diminished),
        (7, IntervalType.Perfect),
        (7, IntervalType.Augmented),
    }

    def __init__(self, diatonic_distance, interval_type):
        """
        Constructor
        
        Args:
          diatonic_distance: number of diatonic tones, 'cdefgab', covered by the interval (inclusive), origin 1
          interval_type: see class IntervalType, or one of the values IntervalType.Major, ...
        """
        if isinstance(interval_type, int):
            interval_type = IntervalType(interval_type)
        self.__interval_type = interval_type
        
        self.__diatonic_distance = (abs(diatonic_distance) - 1) * Interval._sign(diatonic_distance)
        
        octave = Interval._compute_octave(self.__diatonic_distance) 
        
        d_d = abs(self.__diatonic_distance - 7 * octave)
                   
        key = (d_d, interval_type)
        if key not in Interval.VALID_INTERVALS:
            raise Exception('Illegal Interval for {0}-{1}'.format(diatonic_distance, self.interval_type)) 
         
        self.__chromatic_distance = Interval._sign(self.__diatonic_distance) * \
            (Interval.INVERSE_INTERVAL_MAP[(self.interval_type, d_d)]) + 12 * octave
        
    @staticmethod
    def create_interval(pitch_a, pitch_b):
        """
        Create an interval based on two diatonic pitches.
        
        Args:
          pitch_a: the lower diatonic pitch
          pitch_b: the upper diatonic pitch
        Returns:
          the resulting Interval
        """

        if isinstance(pitch_a, str):
            pitch_a = DiatonicPitch.parse(pitch_a)
        if isinstance(pitch_b, str):
            pitch_b = DiatonicPitch.parse(pitch_b)

        if pitch_a is None or pitch_b is None:
            raise Exception('None passed as pitch argument.')
        
        pitch_chromatic_distance = pitch_b.chromatic_distance - pitch_a.chromatic_distance         
        
        # This is just a subtraction of (a_index, a_octave) - (b_index, b_octave)
        # this is origin 0
        tone_index_diff = pitch_b.diatonic_tone.diatonic_index - pitch_a.diatonic_tone.diatonic_index
        octave_diff = pitch_b.octave - pitch_a.octave
            
        # tone_index_diff is the diatonic distance between a and b
        tone_index_diff += octave_diff * 7    # origin 0
        octave = Interval._compute_octave(tone_index_diff) 
        
        # compute the interval type.  Reduce values to within those of INTERVAL_MAP
        d_d = tone_index_diff - 7 * octave
        c_d = pitch_chromatic_distance - 12 * octave  
        # (0, -1) is special, and we need to call it out as a special case.
        (dd, cd) = ((abs(d_d)), -1 if c_d == -1 and d_d == 0 else abs(c_d))
        if (dd, cd) not in Interval.INTERVAL_MAP:
            raise Exception('\'{0}\' and \'{1}\' do not form a valid interval.'.format(pitch_a, pitch_b))
        interval_type = Interval.INTERVAL_MAP[(dd, cd)]
        
        # as usual, the diatonic distance is origin 1, so bump it in the correct sign.
        return Interval((abs(tone_index_diff) + 1) * Interval._sign(tone_index_diff), interval_type)        
    
    @property
    def interval_type(self):
        return self.__interval_type
    
    @property
    def diatonic_distance(self):
        return self.__diatonic_distance
    
    @property
    def chromatic_distance(self):
        return self.__chromatic_distance
    
    def is_same(self, other_interval):
        """
        Determine if this interval is the same as another.
        
        Args:
          other_interval: (Interval) that we compare to
        Returns: True?False
        """
        if other_interval is None:
            return False
        if not isinstance(other_interval, self.__class__):
            raise Exception('Cannot compare interval with {0}'.format(type(other_interval)))
        return self.interval_type == other_interval.interval_type and \
            self.diatonic_distance == other_interval.diatonic_distance
    
    def get_end_tone(self, diatonic_tone):
        """
        Given a tone and this interval, assume the tone is the lower tone of the interval.
        Compute the upper tone.
        
        Args:
          diatonic_tone: DiatonicTone
          
        Returns:
          DiatonicTone of upper tone
        """
        
        result = self.get_end_pitch(DiatonicPitch(4, diatonic_tone.diatonic_symbol))
        return result.diatonic_tone if result else None      
        
    def get_end_pitch(self, pitch):
        """
        Given a pitch and this interval, Assuming pitch is the starting pitch of the interval,
        compute the end pitch.
        
        Args:
          pitch: DiatonicPitch
          
        Returns:
          DiatonicPitch of end tone
        """
        diatonic_dist = pitch.diatonic_distance() + self.diatonic_distance
        tone_index = diatonic_dist % 7
        end_pitch_string = DiatonicTone.get_diatonic_letter(tone_index) 
        end_pitch_octave = diatonic_dist // 7
        
        chromatic_dist = pitch.chromatic_distance + self.chromatic_distance
        
        normal_pitch = DiatonicPitch(end_pitch_octave, DiatonicFoundation.get_tone(end_pitch_string))
        
        alteration = chromatic_dist - normal_pitch.chromatic_distance
        
        end_pitch_string += DiatonicTone.augmentation(alteration)
        
        return DiatonicPitch.parse(end_pitch_string + ':' + str(end_pitch_octave)) 
    
    def get_start_tone(self, diatonic_tone):
        """
        Given a tone and this interval, assume the pitch is the upper tone of the interval.
        Compute the lower tone.
        
        Args:
          diatonic_tone: DiatonicTone
          
        Returns:
          DiatonicTone of the lower tone
        """
        result = self.get_start_pitch(DiatonicPitch(4, diatonic_tone.diatonic_symbol))
        return result.diatonic_tone if result else None 
     
    def get_start_pitch(self, pitch):
        """
        Given a pitch and this interval, assume the pitch is the upper tone of the interval.
        Compute the lower pitch.
        
        Args:
          pitch: DiatonicPitch
          
        Returns:
          DiatonicPitch of the lower tone
        """
        return (self.negation()).get_end_pitch(pitch)
    
    def semitones(self):
        """
        Compute the number of semitones encompassed by this interval;
        Algorithm: translate into interval [C-X] based on diatonic distance, then calculate semitones
                   based on that interval and augmentation offset.
        
        Args:
        Returns: number of semitones.
        """
        
        return abs(self.chromatic_distance)
    
    def __eq__(self, other):        
        return self.is_same(other)
    
    def __ne__(self, other):
        return not self.is_same(other)
    
    def __hash__(self):
        return hash(str(self))
    
    def __add__(self, interval):
        return Interval.add_intervals(self, interval)
    
    def __iadd__(self, interval):
        """
        Override s += y
        
        Args:
          interval: 
        """
        #  The following could throw and exception, that is why it is done.
        i = self + interval
        self.__interval_type = i.interval_type
        self.__chromatic_distance = i.chromatic_distance
        self.__diatonic_distance = i.diatonic_distance
        return self
    
    def negation(self):
        if self.diatonic_distance == 0:
            interval_type = IntervalType.Perfect if self.interval_type == IntervalType.Perfect else \
                IntervalType.Augmented if self.interval_type == IntervalType.Diminished else \
                IntervalType.Diminished
        else:
            interval_type = self.interval_type
        d = (abs(self.diatonic_distance) + 1) * (-1 if self.diatonic_distance > 0 else 1)
        return Interval(d, interval_type)
        
    def inversion(self):
        octave = Interval._compute_octave(self.diatonic_distance)
        octave = octave - 1 if Interval._sign(self.diatonic_distance) == -1 else octave + 1
        (d, c) = (7 * octave - self.diatonic_distance, 12 * octave - self.chromatic_distance)
        (r, s) = Interval._abs(d, c)
        if not (r, s) in Interval.INTERVAL_MAP:              
            raise Exception('No valid inversion for {0}.'.format(self))        
        return Interval((abs(d) + 1) * (1 if d >= 0 else -1), Interval.INTERVAL_MAP[r, s])
    
    def reduction(self): 
        octave = Interval._compute_octave(self.diatonic_distance)  
        (d, c) = (self.diatonic_distance - 7 * octave, self.chromatic_distance - 12 * octave)
        (r, s) = Interval._abs(d, c)
        if not (r, s) in Interval.INTERVAL_MAP:              
            raise Exception('No valid reduction for {0}.'.format(self))        
        return Interval((abs(d) + 1) * Interval._sign(d), Interval.INTERVAL_MAP[r, s])   
    
    @staticmethod
    def available_types(diatonic_distance):
        """
        Per diatonic distance, return the interval types that interval can have,
        
        Args:
          diatonic_distance: (int) 
        Returns:
          An array of IntervalType values.
        """
        if not isinstance(diatonic_distance, int) or diatonic_distance <= 0:
            return []
        return Interval.INTERVAL_AVAILABLE_TYPES[(diatonic_distance - 1) % 7 + 1]

    def is_negative(self):
        return Interval._sign(self.diatonic_distance) == -1
    
    def __str__(self):
        return '{0}{1}:{2}'.format('-' if Interval._sign(self.diatonic_distance) == -1 else '',
                                   IntervalType.short_notation(self.interval_type),
                                   abs(self.diatonic_distance) + 1)

    # Regex used for parsing Interval specification.
    INTERVAL_TYPE = '(P|m|M|A|d)'
    INTERVAL_TYPE_NAME = 'IntervalType'
    INTERVAL_TYPE_TAG = '?P<' + INTERVAL_TYPE_NAME + '>'
    INTERVAL_TYPE_PART = '(' + INTERVAL_TYPE_TAG + INTERVAL_TYPE + ')'
    
    DISTANCE = '[1-9]([0-9]*)'
    DISTANCE_NAME = 'Distance'
    GROUP_DISTANCE_TAG = '?P<' + DISTANCE_NAME + '>'
    DISTANCE_PART = '(' + GROUP_DISTANCE_TAG + DISTANCE + ')'
    
    INTERVAL_SIGN = '(\+|\-)'
    INTERVAL_SIGN_NAME = 'IntervalSign'
    INTERVAL_SIGN_TAG = '?P<' + INTERVAL_SIGN_NAME + '>'
    INTERVAL_SIGN_PART = '(' + INTERVAL_SIGN_TAG + INTERVAL_SIGN + ')'
    
    INTERVAL_PATTERN_STRING = INTERVAL_SIGN_PART + '?' + INTERVAL_TYPE_PART + ':' + DISTANCE_PART
    INTERVAL_PATTERN = re.compile(INTERVAL_PATTERN_STRING)
    
    INTERVAL_LTR_MAP = {'P': IntervalType.Perfect,
                        'A': IntervalType.Augmented,
                        'd': IntervalType.Diminished,
                        'M': IntervalType.Major,
                        'm': IntervalType.Minor}
    
    @staticmethod
    def parse(interval_string):
        """
        Parse a string into an interval.  The string has the format (sign)X:Y
        where X is in {d, m, M, P, A} and Y is an integer.  sign is '-' for negative intervals.
        """
        if not interval_string:
            raise Exception('Unable to parse interval string to completion: {0}'.format(interval_string))
        m = Interval.INTERVAL_PATTERN.match(interval_string)
        if not m:
            raise Exception('Unable to parse interval string to completion: {0}'.format(interval_string))   
        
        interval_type = Interval.INTERVAL_LTR_MAP[m.group(Interval.INTERVAL_TYPE_NAME)] 
        interval_distance = int(m.group(Interval.DISTANCE_NAME))
        
        sign_ltr = m.group(Interval.INTERVAL_SIGN_NAME)
        sign = 1 if sign_ltr is None else (1 if sign_ltr == '+' else -1)
        
        raw_distance = (interval_distance - 1) % 7 + 1
        if interval_type == IntervalType.Perfect:
            if raw_distance != 1 and raw_distance != 4 and raw_distance != 5:
                raise Exception('Illegal interval distance for perfect interval {0}'.format(interval_string))
        if interval_type == IntervalType.Major or interval_type == IntervalType.Minor:
            if raw_distance != 2 and raw_distance != 3 and raw_distance != 6 and raw_distance != 7:
                raise Exception('Illegal interval distance for major/minor interval {0}'.format(interval_string))
            
        # When sign is -1 and interval_distance = 0, we need to reflection_tests the interval
        if sign == -1 and interval_distance == 1:
            interval_type = IntervalType.Augmented if interval_type == IntervalType.Diminished else \
                            IntervalType.Diminished if interval_type == IntervalType.Augmented else IntervalType.Perfect
            
        return Interval(sign * interval_distance, interval_type)
    
    @staticmethod
    def add_intervals(a, b):
        """
        Static method to add two intervals.
        
        Args:
          a: first Interval
          b: second Interval
        Returns:
          combined interval
        Exception: When the combination is impossible, e.g. Dim 2nd + Min 6th
        """
        diatonic_count = a.diatonic_distance + b.diatonic_distance + 1
        chromatic_count = a.chromatic_distance + b.chromatic_distance
        
        b_dc = (diatonic_count - 1) % 7
        octaves = (diatonic_count - 1) // 7
        b_ct = chromatic_count - 12 * octaves        
        
        if (b_dc, b_ct) not in Interval.INTERVAL_MAP:
            raise Exception('Illegal Addition {0} + {1}    ({2}, {3})'.format(a, b, diatonic_count, chromatic_count))
        return Interval(diatonic_count, Interval.INTERVAL_MAP[(b_dc, b_ct)])
    
    @staticmethod
    def _compute_octave(d):
        return 0 if d == 0 else ((abs(d) - 1) // 7) * Interval._sign(d)
    
    @staticmethod
    def _abs(d, c):
        return (d, c) if d >= 0 else (-d, -c)
    
    @staticmethod
    def _sign(x):
        return 1 if x >= 0 else -1

    # The following methods compensate, in some limited cases, for not allowing doubly-augmented/diminished chords.

    @staticmethod
    def calculate_pure_distance(tone1, tone2):
        """
        Calculate the diatonic and chromatic distances between two tones, tone1 to tone2 (as if upwards)
        :param tone1:
        :param tone2:
        :return:
        """
        pitch1 = DiatonicPitch(4, tone1)
        pitch2 = DiatonicPitch(5 if DiatonicPitch.crosses_c(tone1, tone2, True) else 4, tone2)
        cc = pitch2.chromatic_distance - pitch1.chromatic_distance
        dd = (tone2.diatonic_index - tone1.diatonic_index) % 7
        return dd, cc

    @staticmethod
    def calculate_tone_interval(tone1, tone2):
        """
        Calculate interval between tone1 to tone2 assuming closest octave.
        :param tone1:
        :param tone2:
        :return:
        """
        dd, cc = Interval.calculate_pure_distance(tone1, tone2)
        if (dd, cc) not in Interval.INTERVAL_MAP:
            return None
        return Interval(dd + 1, Interval.INTERVAL_MAP[(dd, cc)])

    @staticmethod
    def end_tone_from_pure_distance(tone, dd, cc, up_down=True):
        """
        Given a tone and diatonic/chromatic distances compute the end tone above or below it.
        :param tone:
        :param dd:
        :param cc:
        :param up_down:
        :return:
        """
        new_dd = (tone.diatonic_index + dd) % 7 if up_down else (tone.diatonic_index - dd) % 7
        end_tone = DiatonicToneCache.get_tone(DiatonicTone.get_diatonic_letter(new_dd))
        aug = (cc - (end_tone.placement - tone.placement) % 12) if up_down else \
            (cc - (tone.placement - end_tone.placement) % 12)

        return DiatonicTone.alter_tone_by_augmentation(end_tone, aug)

    @staticmethod
    def _compute_octave1(d):
        return ((abs(d) - 1) // 7) * Interval._sign(d)

    @staticmethod
    def _print_interval_table():
        i_txt = ["P:1", "M:2", "m:3", "M:3", "d:4", "P:4", "P:5", "M:6", "M:7"]
        ivls = list()
        for i in range(0, len(i_txt)):
            ivls.append(Interval.parse(i_txt[i]))
        for i in range(0, len(ivls)):
            s = "[{0}] ".format(i)
            for j in range(0, len(ivls)):
                try:
                    summ = ivls[i] + ivls[j]
                except Exception as e:
                    summ = "X"
                s = s + str(summ) + "  "
            print(s)


# Interval._print_interval_table()
