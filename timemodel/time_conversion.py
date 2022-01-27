"""

File: time_conversion.py

Purpose: To define a set of time-based conversion methods including:
   whole time --> actual time
   actual time --> whole time

"""
from misc.ordered_map import OrderedMap
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from fractions import Fraction
from timemodel.beat_position import BeatPosition
from timemodel.position import Position
from timemodel.duration import Duration


class Element(object):
    
    def __init__(self, ts_or_tempo, position):
        self.__element = ts_or_tempo
        self.__is_tempo = isinstance(ts_or_tempo, Tempo)
        if not self.__is_tempo and not isinstance(ts_or_tempo, TimeSignature):
            raise Exception('Expecting Tempo or TimeSignature, not {0}'.format(type(ts_or_tempo)))
        
        self.__position = position
        self.__position_time = 0
        
    @property
    def element(self):
        return self.__element
    
    @property
    def is_tempo(self):
        return self.__is_tempo
    
    @property
    def position(self):
        return self.__position
        
    @property
    def position_time(self):
        return self.__position_time
    
    @position_time.setter
    def position_time(self, value):
        self.__position_time = value
        
    def is_ts(self):
        return not self.is_tempo
    
    def __str__(self):
        return 'Element({0}, {1}'.format(self.position, self.element)


class TimeConversion(object):
    """
    Time conversion algorithms.
    1) Whole Time --> actual time
    2) actual time --> Wholec Time
    """

    def __init__(self, tempo_line, ts_line, max_position, pickup=Duration(0, 1)):
        """
        Constructor.
        
        Args:
          tempo_line: (EventSequence) of TempoEvent's
          ts_line: (EventSequence) of TimeSignatureEvent's
          max_position: Position of end of whole note time
          pickup: whole note time for a partial initial measure
          
        Assumption:
          tempo_line and ts_line cover position 0
          
        Exceptions:
          If pickup exceeds whole note time of the first time signature.
        """
        self.tempo_line = tempo_line
        self.ts_line = ts_line
        self.__max_position = max_position
        self.__pickup = pickup

        if not isinstance(max_position, Position):
            raise Exception('max_position argument must be Position not \'{0}\'.'.format(type(max_position)))
        
        # check if the pickup exceeds the first TS
        if self.ts_line is None or self.ts_line.is_empty or self.tempo_line is None or self.tempo_line.is_empty:
            raise Exception('Time Signature and Tempo sequences must be non-empty for time conversions.')
        if pickup.duration >= self.ts_line.event(0).object.beats_per_measure * \
                self.ts_line.event(0).object.beat_duration.duration:
            raise Exception(
                'pickup exceeds timing based on first time signature {0}'.format(self.ts_line.event(0).object))
        
        self._build_uniform_element_list()
        self._build_lines()
        self._build_search_trees()
        
        self.__max_time = self.position_to_actual_time(self.max_position)
        
    @property
    def max_position(self):
        return self.__max_position
    
    @property
    def pickup(self):
        return self.__pickup
        
    @property
    def max_time(self):
        return self.__max_time
        
    def _build_uniform_element_list(self):
        self.element_list = [Element(x.object, x.time) for x in self.tempo_line.sequence_list] + \
                            [Element(x.object, x.time) for x in self.ts_line.sequence_list]
        self.element_list.sort(key=lambda p: p.position)
        
    def _build_lines(self):
        """
        Compute the actual time for the tempo and time signature elements.
        """
        current_ts = None
        current_tempo = None
        current_at = 0
        last_position = None
        
        for element in self.element_list:
            if current_ts and current_tempo:
                translated_tempo = current_tempo.effective_tempo(current_ts.beat_duration)
                current_at += (element.position - last_position).duration / \
                              (current_ts.beat_duration.duration * translated_tempo) * 60 * 1000
                element.position_time = current_at
                
            if element.is_tempo:
                current_tempo = element.element
            else:
                current_ts = element.element
            last_position = element.position
            
    def _build_search_trees(self):
        ts_mt_list = []
        ts_time_list = []
        tempo_mt_list = []
        tempo_time_list = []
        
        for element in self.element_list:
            if element.is_tempo:
                tempo_mt_list.append((element.position, element.element))
                tempo_time_list.append((element.position_time, element.element))
            else:
                ts_mt_list.append((element.position, element.element))
                ts_time_list.append((element.position_time, element.element))
                
        self.ts_mt_map = OrderedMap(ts_mt_list)    # whole note time --> TimeSignature
        self.ts_time_map = OrderedMap(ts_time_list)   # actual time --> TimeSignature

        self.tempo_mt_map = OrderedMap(tempo_mt_list)  # whole note time to Tempo
        self.tempo_time_map = OrderedMap(tempo_time_list)   # actual time to Tempo
        
        # Build an ordered map, mapping BeatPosition --> time signature.
        ts_bp_list = []
        (position, ts) = ts_mt_list[0]
        prior_pickup = 0
        measure_tally = 0
        if self.pickup.duration > 0:
            num_beats = self.pickup.duration / ts.beat_duration.duration
            ts_bp_list.append((BeatPosition(0, ts.beats_per_measure - num_beats), ts))
            prior_pickup = num_beats
        else:
            ts_bp_list.append((BeatPosition(0, Fraction(0, 1)), ts))           
        
        for i in range(1, len(ts_mt_list)):
            (position, ts) = ts_mt_list[i]
            (prior_position, prior_ts) = ts_mt_list[i - 1]
            num_beats = (position - prior_position).duration / prior_ts.beat_duration.duration - prior_pickup
            num_measures = int(num_beats / prior_ts.beats_per_measure) + (1 if prior_pickup > 0 else 0)
            measure_tally += num_measures
            prior_pickup = 0
            ts_bp_list.append((BeatPosition(measure_tally, 0), ts))
        self.ts_bp_map = OrderedMap(ts_bp_list)    # beat position --> TimeSignature    

    def position_to_actual_time(self, position):
        """
        Convert a whole time position to it's actual time (in ms) from the beginning.
        
        Args:
          position: a Position in whole time.
        Returns:
          The actual time in ms for the position relative to the beginning.
          
        Note: if the position exceeds max_position, we use max_position
        """
        (tempo_mt_floor, tempo_element) = self.tempo_mt_map.floor_entry(position)
        tempo_time = self.tempo_time_map.reverse_get(tempo_element)
        
        (ts_mt_floor, ts_element) = self.ts_mt_map.floor_entry(position)
        ts_time = self.ts_time_map.reverse_get(ts_element)
        
        start_mt = max(tempo_mt_floor, ts_mt_floor)
        start_time = max(tempo_time, ts_time)
        # at this point, we have:
        #  start_mt: a whole time to start from
        #  start_time: the actual time to start from
        #  tempo_element: the current Tempo
        #  ts_element: the current TimeSignature
        
        delta_mt = min(position, self.max_position) - start_mt
        translated_tempo = tempo_element.effective_tempo(ts_element.beat_duration)
        # time = music_time / (beat_duration * tempo)
        delta_time = (delta_mt.duration / (ts_element.beat_duration.duration * translated_tempo)
                      if delta_mt > 0 else 0) * 60 * 1000
      
        return start_time + delta_time
     
    def actual_time_to_position(self, actual_time):  
        """
        Convert from an actual time (ms) position to a whole time Position
        
        Args:
          actual_time: the actual time (ms) of a position in the music
        Returns:
          the Position corresponding to the actual time.
          
        Note: if actual_time exceeds max_time, we use max_time.
        """
        (tempo_time_floor, tempo_element) = self.tempo_time_map.floor_entry(actual_time)
        tempo_mt = self.tempo_mt_map.reverse_get(tempo_element)
        (ts_time_floor, ts_element) = self.ts_time_map.floor_entry(actual_time)
        ts_mt = self.ts_mt_map.reverse_get(ts_element)
        
        start_mt = max(tempo_mt, ts_mt)
        start_time = max(tempo_time_floor, ts_time_floor)
        # at this point, we have:
        #  start_mt: a whole note time to start from
        #  start_time: the actual time to measure from
        #  tempo_element: the current Tempo
        #  ts_element: the current TimeSignature
        
        delta_time = min(actual_time, self.max_time) - start_time
        if not isinstance(delta_time, Fraction):
            delta_time = Fraction.from_float(delta_time)
        # musicTime = time * tempo * beat_duration
        # Translate tempo using the time signature beat.
        translated_tempo = tempo_element.effective_tempo(ts_element.beat_duration)
        delta_mt = (delta_time * translated_tempo * ts_element.beat_duration.duration / (60 * 1000)) \
            if delta_time > 0 else 0
        
        return start_mt + delta_mt
    
    def bp_to_position(self, beat_position):
        """
        Method to convert a beat position to a whole note time position.
        
        Args:
          beat_position: BeatPosition object given measure, beat number
        Returns:
          the whole note time position for beat_position.
          
        Exceptions:
          for improper beat_position values
        """
        (beginning_bp, ts_element) = self.ts_bp_map.floor_entry(beat_position)
        if beat_position.beat_number >= ts_element.beats_per_measure:
            raise Exception(
                'Illegal beat asked for {0}, ts has 0-{1} beats per measure.'.format(beat_position.beat_number,
                                                                                     ts_element.beats_per_measure - 1))
        
        ts_mt_floor = self.ts_mt_map.reverse_get(ts_element)
        
        delta_mt = ((beat_position.measure_number - beginning_bp.measure_number) * ts_element.beats_per_measure +
                    beat_position.beat_number - beginning_bp.beat_number) * ts_element.beat_duration.duration
        return Position(ts_mt_floor.position + delta_mt)
    
    def position_to_bp(self, position):
        """
        Method to convert a whole note time position to a beat position
        
        Args:
          position: the whole note time position
        Returns:
          the BeatPosition corresponding to the given position
        """
        (ts_mt_floor, ts_element) = self.ts_mt_map.floor_entry(position)
        
        ts_bp = self.ts_bp_map.reverse_get(ts_element)
        
        num_beats = (position - ts_mt_floor).duration / ts_element.beat_duration.duration   # - prior_pickup.duration
        num_measures = int(num_beats / ts_element.beats_per_measure)   # + (1 if prior_pickup.duration > 0 else 0)
        residual_beats = num_beats - num_measures * ts_element.beats_per_measure
        
        # add the measures and beats  to ts_bp
        beats = ts_bp.beat_number + residual_beats
        measures = ts_bp.measure_number + num_measures
        if beats >= ts_element.beats_per_measure:
            beats -= ts_element.beats_per_measure
            measures += 1
                    
        return BeatPosition(measures, beats)
