"""

File: tertian_chord.py

Purpose: Defines a class to represent a tertian chord

"""
from harmonicmodel.chord import Chord
from tonalmodel.interval import Interval
from tonalmodel.diatonic_pitch import DiatonicPitch


class TertianChord(Chord):
    """
    Class that defines a tertian chord
    This class create it tones based on differing specifications found in TertianChordTemplate:
    1) If root is given by a diatonic tone (and chord type), the diatonic tonality is not used,
       and strict interval specs decide the other notes.
    2) If root is given by diatonic tonality and scale reference, 
       a) If the chord type is given, the tones are built as in 1) but with the root determined by
          scale degree on tonality.
       b) If the chord type is note given, the tones are built on the tonality itself.  The chord type determined by
          the tones.
       
    Inversion results in a re-ordering of the tone, making the inversion tone the first tone.
    
    The result self.tones is a list of duplets (diatonic_tone, interval)
    """

    def __init__(self, tertian_chord_template, diatonic_tonality=None):
        """
        Constructor.
        Args:
          tertian_chord_template: TertianChordTemplate
          diatonic_tonality: DiatonicTonality (used in scale degree chord formation)
        """
        Chord.__init__(self, tertian_chord_template, diatonic_tonality)    
        
        self.__tones = []
        self.__chord_type = self.chord_template.chord_type
        
        self.__root_tone = self.chord_template.diatonic_basis
        
        if self.chord_template.diatonic_basis:
            self.__create_chord_on_diatonic(self.root_tone)
        else:
            if not self.diatonic_tonality:
                raise Exception(
                    'Diatonic tonality must be specified for chords based on scale degree: {0}'.
                    format(str(self.chord_template)))
            if self.chord_type:
                self.__create_chord_on_scale_degree_with_chord_type()
            else:
                self.__create_chord_on_scale_degree()
            
    def __create_chord_on_diatonic(self, diatonic_tone):
        self.chord_basis = []
        for interval in self.chord_template.base_intervals:
            tone = interval.get_end_tone(diatonic_tone)
            self.__tones.append((tone, interval))
            self.chord_basis.append(interval)
          
        for interval in self.chord_template.tension_intervals:
            tone = interval.get_end_tone(diatonic_tone)   
            self.__tones.append((tone, interval))
            
        self.__set_inversion()
        
    def __create_chord_on_scale_degree(self):
        from harmonicmodel.tertian_chord_template import TertianChordTemplate
        root_index = self.chord_template.scale_degree - 1
        tone_scale = self.diatonic_tonality.annotation
        
        self.chord_basis = []
        base_tone = None
        for i in range(0, 3):
            tone = tone_scale[(root_index + 2 * i) % (len(tone_scale) - 1)]
            if i == 0:
                base_tone = tone
                       
            pitch_a = DiatonicPitch(1, tone_scale[root_index].diatonic_symbol)
            b_octave = 2 if base_tone.diatonic_index > tone.diatonic_index else 1
            pitch_b = DiatonicPitch(b_octave, tone.diatonic_symbol)
            interval = Interval.create_interval(pitch_a, pitch_b)
            self.chord_basis.append(interval)
            
            self.__tones.append((tone, interval))
        self.__set_inversion()
        
        self.__chord_type = TertianChordTemplate.get_chord_type(self.chord_basis)    
        
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
        elif self.chord_template.inversion_interval:
            # find the interval

            for i in range(0, len(self.chord_basis)):
                if self.chord_basis[i].is_same(self.chord_template.inversion_interval):
                    invert_id = i + 1
                    break
            if invert_id != -1 and self.chord_template.tension_intervals:
                for i in range(0, len(self.chord_template.tension_intervals)):
                    if self.chord_template.tension_intervals[i] == self.chord_template.inversion_interval:
                        invert_id = i + 1 + len(self.chord_basis)
                        break
            if invert_id == -1:
                raise Exception(
                    "Could not find interval {0} for chord off template {1}".
                    format(self.chord_template.inversion_interval, self.chord_template))
            # remove the cited index
        item = self.__tones[invert_id - 1]
        self.__tones.remove(item)
        self.__tones.insert(0, item)
    
    @property        
    def tones(self):
        new_list = []
        new_list.extend(self.__tones)
        return new_list
    
    @property
    def chord_type(self):
        return self.__chord_type
    
    @property
    def root_tone(self):
        return self.__root_tone
    
    def sorted_tones(self):
        return sorted(self.tones, key=lambda tone: tone[1].semitones())
    
    def __str__(self):
        return '{0} [{1}]'.format(str(self.chord_template),
                                  ', '.join(str(tone[0].diatonic_symbol) for tone in self.tones))
