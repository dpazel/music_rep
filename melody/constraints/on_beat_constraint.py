"""

File: on_beat.py

Purpose: Defines a class indicating for some actor that it must adhere to a given beat constraint.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.time_signature import BeatType
from timemodel.position import Position
from timemodel.time_conversion import TimeConversion


class OnBeatConstraint(AbstractConstraint):
    """
    Constraint that forces one actor to be either on a specifc beat, or on a specific kind of beat (weak/strong)
    """

    def __init__(self, actor, beats_or_bt):
        """
        Constructor.
        :param actor: Note
        :param beats_or_bt: int or list of int's for beat specification (origin 0) or a BeatType
        """
        self.__beat_ids = None
        self.__beat_type = None
        if isinstance(beats_or_bt, int):
            self.__beat_ids = [beats_or_bt]
        elif isinstance(beats_or_bt, list):
            self.__beat_ids = list(beats_or_bt)
        elif isinstance(beats_or_bt, BeatType):
            self.__beat_type = beats_or_bt

        AbstractConstraint.__init__(self, [actor])

    def clone(self, new_actors=None):
        return OnBeatConstraint(new_actors if new_actors is not None else self.actors,
                                self.beat_ids if self.beat_ids is not None else self.beat_type)

    @property
    def beat_ids(self):
        return self.__beat_ids

    @property
    def actor(self):
        return self.actors[0]

    @property
    def beat_type(self):
        return self.__beat_type

    def verify(self, pdi):
        """
        Verify that the beat constraint holds.
        :param pdi: PositionDeltaInfo.
        :return: True/False on meeting constraint.
        """
        conversion = TimeConversion(pdi.tempo_event_sequence, pdi.ts_event_sequence, Position(pdi.line_duration()))
        new_position = pdi.correct_position(self.actor.get_absolute_position())
        beat_position = conversion.position_to_bp(new_position)
        if beat_position.beat_fraction > 0:
            return False

        beat = beat_position.beat
        ts = pdi.ts_event_sequence.floor_event(new_position).object
        beat_list = self.beat_ids if self.beat_ids is not None else ts.beats_matching(self.beat_type)
        return beat in beat_list

    def values(self, pdi, note):
        position = pdi.correct_position(note.get_absolute_position())  # position should be adjusted
        ts = pdi.ts_event_sequence.floor_event(position).object
        beat_position = TimeConversion(pdi.tempo_event_sequence, pdi.ts_event_sequence, Position(pdi.line_duration())).\
            position_to_bp(position)
        num_beats = ts.beats_per_measure if beat_position.beat_fraction > 0 else ts.beats_per_measure - 1
        beat_index = (beat_position.beat + 1) % ts.beats_per_measure
        delta_t = ts.beat_duration if beat_position.beat_fraction == 0 else \
            ts.beat_duration * (1 - beat_position.beat_fraction)
        deltas = set()
        for i in range(0, num_beats):
            if (self.beat_ids is not None and beat_index in self.beat_ids) or \
               (self.beat_type is not None and self.beat_type == ts.beat_type(beat_index)):
                deltas.add(delta_t)
            delta_t += ts.beat_duration
            beat_index = (beat_index + 1) % ts.beats_per_measure

        return deltas
