"""
File: pitch_fit_function.py

Purpose: Support for remapping a pitch at a position given a function.

"""
from structure.time_signature import BeatType
from timemodel.duration import Duration
from timemodel.position import Position
from timemodel.time_conversion import TimeConversion


class PitchFitFunction(object):
    SCALAR_BIAS_WEIGHT = 0.60

    def __init__(self, pitch_function, tempo_sequence, ts_sequence, hct=None):
        self.__pitch_function = pitch_function
        self.__hct = hct
        self.__tempo_sequence = tempo_sequence
        self.__ts_sequence = ts_sequence

    @property
    def pitch_function(self):
        return self.__pitch_function

    @property
    def hct(self):
        return self.__hct

    @property
    def tempo_sequence(self):
        return self.__tempo_sequence

    @property
    def ts_sequence(self):
        return self.__ts_sequence

    def __call__(self, position):
        return self.eval(position)

    def eval(self, position):
        if position is None:
            raise Exception('Expecting Positino paramter, not None.')
        if not isinstance(position, Position):
            raise Exception('Expecting Position parameter, found {0}.'.format(type(position)))

        hc = self.hct[position.position] if self.hct is not None else None
        # TODO:
        # if hc is None:
        #     raise Exception('Cannot find hc at position {0}'.format(position))

        candidate_pitches = list()
        for p in self.pitch_function.eval_as_pitch(position.position):
            e = PitchFitFunction._get_tonal_equivalent(p, hc) if hc is not None else None
            candidate_pitches.append((e, True) if e is not None else (p, False))

        if len(candidate_pitches) == 0:
            return None

        v_note_beat_position = self._get_beat_position(position)

        # If one solution pitch
        if len(candidate_pitches) == 1:
            # if is scalar, use it
            if candidate_pitches[0][1]:
                return candidate_pitches[0][0]
            # non-scalar
            # if on beat and half step off from chord tone, do not use
            if v_note_beat_position is not None and v_note_beat_position == BeatType.Strong:
                if hc is not None and PitchFitFunction._pitch_is_halfstep_off_chord(candidate_pitches[0][0], hc):
                    return None
            # otherwise use
            return candidate_pitches[0][0]

        # if 2 pitch solution
        if len(candidate_pitches) == 2:
            function_value = self.pitch_function.eval_as_chromatic_distance(position.position)
            interp = self.pitch_function.pitch_range_interpreter
            # If both scalar
            if candidate_pitches[0][1] and candidate_pitches[1][1]:
                index = min(enumerate(candidate_pitches),
                            key=lambda x: abs(interp.value_for(x[1][0]) - function_value))[0]
                # return pitch closest to curve value
                return candidate_pitches[index][0]
            elif not candidate_pitches[0][1] and not candidate_pitches[1][1]:
                index = min(enumerate(candidate_pitches),
                            key=lambda x: abs(interp.value_for(x[1][0]) - function_value))[0]
                pitch = candidate_pitches[index][1]
                # if on beat and half step off from chord tone, do not use
                if v_note_beat_position is not None and hc is not None:
                    if PitchFitFunction._pitch_is_halfstep_off_chord(pitch, hc):
                        return None
                # otherwise use
                return pitch
            else:
                # TODO: We have to question if we should always return the scalar over non-scalar.
                scalar_pitch = candidate_pitches[0][0] if candidate_pitches[0][1] \
                    else candidate_pitches[1][0]
                nonscalar_pitch = candidate_pitches[0][0] if candidate_pitches[1][1] \
                    else candidate_pitches[1][0]
                scalar_bias = (interp.value_for(scalar_pitch) - function_value) / \
                    abs(interp.value_for(scalar_pitch) - interp.value_for(nonscalar_pitch))
                if v_note_beat_position is not None or scalar_bias <= PitchFitFunction.SCALAR_BIAS_WEIGHT:
                    return scalar_pitch
                else:
                    return nonscalar_pitch
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
        # TimeConversion needs a max time - in this limited context use a very small duration over position.
        p = position + Duration(1, 32)
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
