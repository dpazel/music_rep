"""

File: quartal_chord.py

Purpose: Representing an instance of a quartal chord.

"""
from harmonicmodel.chord import Chord
from tonalmodel.interval import Interval, IntervalType
from tonalmodel.diatonic_pitch import DiatonicPitch


class QuartalChord(Chord):
    """
    Class to represent an instance of a quartal chord.
    """

    def __init__(self, quartal_chord_template, diatonic_tonality=None):
        """
        Constructor.
        Args:
          quartal_chord_template: SecundalChordTemplate
          diatonic_tonality: DiatonicTonality (used in scale degree chord formation)
        """
        from harmonicmodel.quartal_chord_template import QuartalChordTemplate
        Chord.__init__(self, quartal_chord_template, diatonic_tonality) 
        
        self.__tones = []
        self.__chord_type = self.chord_template.chord_type
        
        self.__root_tone = self.chord_template.diatonic_basis 
        
        if self.__root_tone:
            if len(self.chord_template.base_intervals) != 0:
                self.__create_chord_on_diatonic(self.root_tone)
            else:
                if self.diatonic_tonality is None:
                    self.__create_chord_on_root_no_base_intervals(self.root_tone)
                else:
                    self.__create_chord_on_diatonic_tonality(self.root_tone, self.diatonic_tonality)
        else:
            if not self.diatonic_tonality:
                raise Exception('Diatonic tonality must be specified for chords based on scale degree: {0}'.
                                format(str(self.chord_template)))
            if self.chord_template.base_intervals:
                self.__create_chord_on_scale_degree_with_chord_type()
            else:
                self.__create_chord_on_scale_degree() 
        
        self.__set_inversion() 
        self.__chord_type = QuartalChordTemplate.get_chord_type(self.chord_basis)
        
    @property
    def chord_type(self):
        return self.__chord_type
    
    @property
    def root_tone(self):
        return self.__root_tone
    
    @property
    def tones(self):
        new_list = []
        new_list.extend(self.__tones)
        return new_list 
    
    def __create_chord_on_diatonic(self, diatonic_tone):
        self.chord_basis = []
        current_tone = diatonic_tone
        for interval in self.chord_template.base_intervals:               
            tone = interval.get_end_tone(current_tone)
            self.__tones.append((tone, interval))
            self.chord_basis.append(interval)
            current_tone = tone

    def __create_chord_on_root_no_base_intervals(self, diatonic_tone):
        # Assume MM or MajMaj
        self.chord_basis = []
        current_tone = diatonic_tone
        intervals = [Interval(1, IntervalType.Perfect),
                     Interval(4, IntervalType.Perfect),
                     Interval(4, IntervalType.Perfect)]
        for i in range(0, 3):
            tone = intervals[i].get_end_tone(current_tone)
            self.__tones.append((tone, intervals[i]))
            self.chord_basis.append(intervals[i])
            current_tone = tone
                    
    def __create_chord_on_diatonic_tonality(self, diatonic_tone, diatonic_tonality):
        if not diatonic_tonality:
            raise Exception("Cannot base quartal chord on tone {0} without tonality.".
                            format(diatonic_tone.diatonic_symbol))
        # The tonality must include this tone.
        tone_scale = diatonic_tonality.annotation
        found_index = -1
        for i in range(0, len(tone_scale)):
            if diatonic_tone == tone_scale[i]:
                found_index = i
                break
        if found_index == -1:
            raise Exception("For quartal chord based on tone {0}, tone must be in given tonality {1}".
                            format(diatonic_tone.diatonic_symbol, diatonic_tonality))
        self.chord_basis = []
        basis_tone = tone_scale[found_index]
        for i in range(0, 3):               
            tone = tone_scale[(found_index + 3 * i) % (len(tone_scale) - 1)]
            pitch_a = DiatonicPitch(1, basis_tone.diatonic_symbol)
            b_octave = 2 if basis_tone.diatonic_index > tone.diatonic_index else 1
            pitch_b = DiatonicPitch(b_octave, tone.diatonic_symbol)
            interval = Interval.create_interval(pitch_a, pitch_b)
            self.chord_basis.append(interval)
            
            self.__tones.append((tone, interval))
            basis_tone = tone 
        
    def __create_chord_on_scale_degree(self):
        root_index = self.chord_template.scale_degree - 1
        tone_scale = self.diatonic_tonality.annotation
        
        basis_tone = tone_scale[root_index]

        self.__create_chord_on_root_no_base_intervals(basis_tone)
        
    def __create_chord_on_scale_degree_with_chord_type(self):
        root_index = self.chord_template.scale_degree - 1
        tone_scale = self.diatonic_tonality.annotation
        self.__root_tone = tone_scale[root_index]
        
        self.__create_chord_on_diatonic(self.__root_tone)
    
    def __set_inversion(self):
        invert_id = -1
        if self.chord_template.inversion:
            if self.chord_template.inversion == 1:
                return
            invert_id = self.chord_template.inversion
        # remove the cited index
        item = self.__tones[invert_id - 1]
        self.__tones.remove(item)
        self.__tones.insert(0, item)   
        
    def __str__(self):
        return '{0} [{1}]'.format(str(self.chord_template),
                                  ', '.join(str(tone[0].diatonic_symbol) for tone in self.tones))
