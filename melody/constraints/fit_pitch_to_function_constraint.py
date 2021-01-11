"""

File: fit_pitch_to_function_constraint.py

Purpose: Pitch fitting to a curve given by a pitch function.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from structure.time_signature import BeatType
from timemodel.time_conversion import TimeConversion

'''
Notes on FitPitchToFunctionConstraint:

The key for the new constraint is the call to 'eval_as_pitch', which returns one or two pitches nearest to the 
reshape curve.

Case 1: Exactly one pitch.
If pitch is scalar, use
If pitch is non-scalar - if on-beat and pitch is 1/2 step from any chordal tone, do not use, else use

Case 2: Two notes
If both are scalar, use the closest to the curve.
If both are non-scalar, use the nearest to curve, and apply as in case 1   (example, A, Bb in C-)
If one is scalar and the other not:
   If the scalar is on-beat or is within the scalar bias weight, use it
   Otherwise use the non-scalar
'''


class FitPitchToFunctionConstraint(AbstractConstraint):
    """
    FitPitchToFunctionConstraint: Class to constrain pitch assignment to align to a given pitch map [time --> pitch]
    """

    SCALAR_BIAS_WEIGHT = 0.60

    def __init__(self, actor_note, pitch_function, tempo_sequence, ts_sequence):
        """
        Constructor
        :param actor_note: Note
        :param pitch_function: FunctionPitchRange
        :param tempo_sequence: TempoEventSequence
        :param ts_sequence: EventSequence
        """
        AbstractConstraint.__init__(self, [actor_note])

        self.__pitch_function = pitch_function
        self.__tempo_sequence = tempo_sequence
        self.__ts_sequence = ts_sequence

        self.note_position = self.actor_note.get_absolute_position()
        # value of function at this position.
        self.function_value = self.pitch_function.eval_as_chromatic_distance(self.note_position.position)

    @property
    def actor_note(self):
        return self.actors[0]

    @property
    def pitch_function(self):
        return self.__pitch_function

    @property
    def ts_sequence(self):
        return self.__ts_sequence

    @property
    def tempo_sequence(self):
        return self.__tempo_sequence

    def __str__(self):
        return 'f_p_t_f_c actor={0} eval={1}.'.format(self.actor_note,
                                                      ', '.join(str(p) for p in self.pitch_function.eval_as_pitch(
                                                          self.actor_note.get_absolute_position().position)))

    def clone(self, new_actors=None):
        return FitPitchToFunctionConstraint(new_actors[0] if new_actors is not None else self.actor_note,
                                            self.pitch_function, self.tempo_sequence, self.ts_sequence)

    def verify(self, p_map):
        if self.actor_note not in p_map:
            raise Exception('Improper parameter map in fit pitch to function constraint.')
        if p_map[self.actor_note].note is None:
            return False

        hc = p_map[self.actor_note].policy_context.harmonic_context
        values = self._compute_values(self.actor_note, hc)
        if values is None or len(values) == 0:
            return False

        return p_map[self.actor_note].note.diatonic_pitch in {note.diatonic_pitch for note in values}

    def values(self, p_map, v_note):
        index = self.actors.index(v_note) if v_note in self.actors else None
        if index is None:
            raise Exception('Cannot find v_note in constraints actors')

        if p_map[v_note].note is not None:
            return {p_map[v_note].note}

        return self._compute_values(v_note, p_map[v_note].policy_context.harmonic_context)

    def _compute_values(self, v_note, hc):

        self.candidate_pitches = list()
        for p in self.pitch_function.eval_as_pitch(self.note_position.position):
            e = FitPitchToFunctionConstraint._get_tonal_equivalent(p, hc)
            self.candidate_pitches.append((e, True) if e is not None else (p, False))

        if len(self.candidate_pitches) == 0:
            return set()

        v_note_beat_position = self._get_beat_position(v_note.get_absolute_position())

        # If one solution pitch
        if len(self.candidate_pitches) == 1:
            # if is scalar, use it
            if self.candidate_pitches[0][1]:
                return {Note(self.candidate_pitches[0][0], v_note.base_duration, v_note.num_dots)}
            # non-scalar
            # if on beat and half step off from chord tone, do not use
            if v_note_beat_position is not None and v_note_beat_position == BeatType.Strong:
                if FitPitchToFunctionConstraint._pitch_is_halfstep_off_chord(self.candidate_pitches[0][0], hc):
                    return set()
            # otherwise use
            return {Note(self.candidate_pitches[0][0], v_note.base_duration, v_note.num_dots)}

        # if 2 pitch solution
        if len(self.candidate_pitches) == 2:
            # If both scalar
            if self.candidate_pitches[0][1] and self.candidate_pitches[1][1]:
                interp = self.pitch_function.pitch_range_interpreter
                index = min(enumerate(self.candidate_pitches), key=lambda x: abs(interp.value_for(x[1][0]) - self.function_value))[0]   # CHECK ERROR
                # return pitch closest to curve value
                return {Note(self.candidate_pitches[index][0], v_note.base_duration, v_note.num_dots)}
            elif not self.candidate_pitches[0][1] and not self.candidate_pitches[1][1]:
                index = min(enumerate(self.candidate_pitches), key=lambda x: abs(interp.value_for(x[1][0]) - self.function_value))[0]
                pitch = self.candidate_pitches[index]
                # if on beat and half step off from chord tone, do not use
                if v_note_beat_position is not None:
                    if FitPitchToFunctionConstraint._pitch_is_halfstep_off_chord(pitch, hc):
                        return set()
                # otherwise use
                return {Note(pitch, v_note.base_duration, v_note.num_dots)}
            else:
                scalar_pitch = self.candidate_pitches[0][0] if self.candidate_pitches[0][1] \
                    else self.candidate_pitches[1][0]
                nonscalar_pitch = self.candidate_pitches[0][0] if self.candidate_pitches[1][1] \
                    else self.candidate_pitches[1][0]
                scalar_bias = (scalar_pitch.chromatic_distance - self.function_value) /\
                    abs(scalar_pitch.chromatic_distance - nonscalar_pitch.chromatic_distance)
                if v_note_beat_position is not None or scalar_bias <= FitPitchToFunctionConstraint.SCALAR_BIAS_WEIGHT:
                    return {Note(scalar_pitch, v_note.base_duration, v_note.num_dots)}
                else:
                    return {Note(nonscalar_pitch, v_note.base_duration, v_note.num_dots)}
        else:
            raise Exception('Internal error - more than 2 candidate pitches.')

    @staticmethod
    def _get_tonal_equivalent(pitch, hc):
        enharmonics = pitch.enharmonics()
        for e in enharmonics:
            if e.diatonic_tone in hc.tonality.annotation:
                return e
        return None

    def _get_beat_position(self, position):
        ts = self.ts_sequence.floor_event(position).object
        p = position + self.actor_note.duration
        beat_position = TimeConversion(self.tempo_sequence, self.ts_sequence, p).position_to_bp(position)

        beat_type = ts.beat_type(beat_position.beat) if beat_position.beat_fraction == 0 else None
        return beat_type

    @staticmethod
    def _pitch_is_halfstep_off_chord(pitch, hc):
        tones = hc.chord.tones
        for tone in tones:
            dist = abs(tone[0].placement - pitch.diatonic_tone.placement)
            if dist == 1 or dist == 11:
                return True

        return False
