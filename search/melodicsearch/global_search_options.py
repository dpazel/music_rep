

class GlobalSearchOptions(object):
    """
    Options:
    1) structural_match: If true, beam and tuples must match between pattern and target.
    2) hct_match_tonality_key_tone: If true, hct's must match on key tone but not necessarily modality.
    3) hct_match_tonality_modality: If true, hct's must match on modality but not necessarily key tone.
    4) hct_match_relative_chord: If true, hct's must match on chord degree relative to tonalities.
    5) note_match_scalar_precision: If true, scalar tones must match on scalar degree.
    6) note_match_chordal: If true, if pattern note is chordal, so must be the corresponding target note.
    7) note_match_chordal_precision: if true, chordal notes must match on chordal interval. (req. note_match_chordal)
    8) note_match_non_scalar_precision: If true, non-scalars must match on interval to root tonality tone.
    9) note_match_non_scalar_to_scalar: If true, non-scalar pattern must match to non-scalar target.
    """

    def __init__(self, structural_match=True,
                 hct_match_tonality_key_tone=False,
                 hct_match_tonality_modality=False,
                 hct_match_relative_chord=False,
                 note_match_scalar_precision=False,
                 note_match_chordal=False,
                 note_match_chordal_precision=False,
                 note_match_non_scalar_precision=False,
                 note_match_non_scalar_to_scalar=False):

        self.__structural_match = structural_match
        self.__hct_match_tonality_key_tone = hct_match_tonality_key_tone
        self.__hct_match_tonality_modality = hct_match_tonality_modality
        self.__hct_match_relative_chord = hct_match_relative_chord

        self.__note_match_scalar_precision = note_match_scalar_precision
        self.__note_match_chordal = note_match_chordal
        self.__note_match_chordal_precision = note_match_chordal_precision
        self.__note_match_non_scalar_precision = note_match_non_scalar_precision
        self.__note_match_non_scalar_to_scalar = note_match_non_scalar_to_scalar

        if note_match_chordal_precision and not note_match_chordal:
            raise Exception('note_match_chordal_precision requires note_match_chordal.')

    @property
    def structural_match(self):
        return self.__structural_match

    @property
    def hct_match_tonality_key_tone(self):
        return self.__hct_match_tonality_key_tone

    @property
    def hct_match_tonality_modality(self):
        return self.__hct_match_tonality_modality

    @property
    def hct_match_relative_chord(self):
        return self.__hct_match_relative_chord

    @property
    def note_match_scalar_precision(self):
        return self.__note_match_scalar_precision

    @property
    def note_match_chordal(self):
        return self.__note_match_chordal

    @property
    def note_match_chordal_precision(self):
        return self.__note_match_chordal_precision

    @property
    def note_match_non_scalar_precision(self):
        return self.__note_match_non_scalar_precision

    @property
    def note_match_non_scalar_to_scalar(self):
        return self.__note_match_non_scalar_to_scalar
