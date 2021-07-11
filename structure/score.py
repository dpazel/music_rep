"""

File: score.py

Purpose: Class representing a score, consisting of a number of instrument voices. It also retains event
         sequences for tempo and time, which are global over all the voices.

"""

from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event_sequence import TimeSignatureEventSequence
from timemodel.time_conversion import TimeConversion
from timemodel.duration import Duration
from timemodel.position import Position
from misc.interval import Interval

from structure.instrument_voice import InstrumentVoice
from harmoniccontext.harmonic_context_track import HarmonicContextTrack


class Score(object):
    """
    Class representing a score, consisting of a number of instrument voices. It also retains event
         sequences for tempo and time, which are global over all the voices.
    """

    def __init__(self):
        """
        Constructor.
        """
        
        self.__instrument_voices = list()
        # map from instrument class to the instrument voices added.
        self.class_map = dict()
        # map instrument class name to InstrumentClass
        self.name_class_map = dict()
        # HCT not utilized, TODO
        self.__hct = HarmonicContextTrack()
        
        self.__tempo_sequence = TempoEventSequence()
        self.__time_signature_sequence = TimeSignatureEventSequence()
        
    @property
    def tempo_sequence(self):
        return self.__tempo_sequence
    
    @property
    def time_signature_sequence(self):
        return self.__time_signature_sequence

    @property
    def hct(self):
        return self.__hct
        
    def add_instrument_voice(self, instrument_voice):
        if not isinstance(instrument_voice, InstrumentVoice):
            raise Exception('parameter must be InstrumentVoice type not {0}'.format(type(instrument_voice)))
        instrument_family = instrument_voice.instrument.parent
        instrument_class = instrument_family.parent
        
        # add the name to class map if not already there.
        if instrument_class.name.upper() not in self.name_class_map:
            self.name_class_map[instrument_class.name.upper()] = instrument_class
        
        # Add the map key to class_map if not there,
        #    then append the given instrument voice to to map target.
        if instrument_class not in self.class_map:
            self.class_map[instrument_class] = []
        self.class_map[instrument_class].append(instrument_voice)
        
        # Add the instrument voice to the general list.
        self.__instrument_voices.append(instrument_voice)
            
    def get_class_instrument_voices(self, class_name):
        if class_name.upper() not in self.name_class_map:
            return []
        else:
            return list(self.class_map[class_name.upper()])
    
    @property    
    def instrument_voices(self):
        return list(self.__instrument_voices)
    
    @property
    def instrument_classes(self):
        return [k for (k, _) in self.class_map.items()]

    def get_instrument_voice(self, instrument_name):
        answer = []
        for inst_voice in self.__instrument_voices:
            if inst_voice.instrument.name.upper() == instrument_name.upper():
                answer.append(inst_voice)
        return answer
    
    def remove_instrument_voice(self, instrument_voice):
        if instrument_voice not in self.__instrument_voices:
            raise Exception('Attempt to remove voice {0} which does not exist'.format(
                instrument_voice.instrument.name))
        self.__instrument_voices.remove(instrument_voice)
        
        class_name = instrument_voice.instrument.parent.parent.name
        class_object = self.name_class_map[class_name.upper()]
        class_list = self.class_map[class_object]
        class_list.remove(instrument_voice)
        if len(class_list) == 0:
            self.name_class_map.pop(class_name.upper())
            self.class_map.pop(class_object)
        
    def remove_instrument_class(self, class_name):
        if class_name.upper() not in self.name_class_map:
            raise Exception('Attempt to remove class voices {0} which do not exist'.format(class_name))
        
    @property
    def duration(self):
        return self.length()
    
    def length(self):
        duration = Duration(0)
        for voice in self.__instrument_voices:
            duration = voice.duration if voice.duration > duration else duration
        return duration
    
    def real_time_duration(self):
        interval = Interval(0, self.duration)
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        return conversion.position_to_actual_time(interval.upper) 
        
    def get_notes_by_wnt_interval(self, interval):
        """
        Get all the notes in the score by interval:  Return dict structure as follows:
            instrument_voice --> {voice_index --> [notes]}
        """
        answer = {}
        for instrument_voice in self.__instrument_voices:
            answer[instrument_voice] = instrument_voice.get_notes_by_interval(interval)
        return answer
    
    def get_notes_by_rt_interval(self, interval):
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        wnt_interval = Interval(conversion.actual_time_to_position(interval.lower),
                                conversion.actual_time_to_position(interval.upper))
        return self.get_notes_by_wnt_interval(wnt_interval)
    
    def get_notes_by_bp_interval(self, interval):
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        wnt_interval = Interval(conversion.bp_to_position(interval.lower), conversion.bp_to_position(interval.upper))
        return self.get_notes_by_wnt_interval(wnt_interval)
    
    def get_notes_starting_in_wnt_interval(self, interval):
        """
        Get all the notes starting in the score by whole note time interval:  Return dict structure as follows:
            instrument_voice --> {voice_index --> [notes]}
        """
        answer = {}
        for instrument_voice in self.__instrument_voices:
            answer[instrument_voice] = instrument_voice.get_notes_starting_in_interval(interval)
        return answer
    
    def get_notes_starting_in_rt_interval(self, interval):
        """
        Get all notes starting in the score by an interval based on real time:  Return dict structure as follows:
            instrument_voice --> {voice_index --> [notes]}
        """
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        wnt_interval = Interval(conversion.actual_time_to_position(interval.lower),
                                conversion.actual_time_to_position(interval.upper))
        return self.get_notes_starting_in_wnt_interval(wnt_interval)
    
    def get_notes_starting_in_bp_interval(self, interval):
        """
        Get all notes starting in the score by an interval based on beat position:  Return dict structure as follows:
            instrument_voice --> {voice_index --> [notes]}
        """
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        wnt_interval = Interval(conversion.bp_to_position(interval.lower), conversion.bp_to_position(interval.upper))
        return self.get_notes_starting_in_wnt_interval(wnt_interval)
    
    @property 
    def beat_duration(self):
        duration = self.duration
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        return conversion.position_to_bp(Position(duration.duration))
    
    @property 
    def real_duration(self):
        duration = self.duration
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        return conversion.position_to_actual_time(Position(duration.duration))
