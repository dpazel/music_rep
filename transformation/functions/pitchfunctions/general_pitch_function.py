"""

File: general_pitch_function.py

Purpose: Class defining a pitch function wherein pitch mappings are explicitly given.

"""
from function.discrete_function import DiscreteFunction
from tonalmodel.diatonic_pitch import DiatonicPitch


class GeneralPitchFunction(DiscreteFunction):
    """
    Class implementation of a function between two discrete sets of pitches.
    """

    # Indication of non-functional pitch mapping.  For example, mapping octatonic to pentatonic, some
    # pitches map to NONE as opposed to some legitimate pentatonic tone that in context does not make sense.
    # A return of None from the map indicates to the user that he/she must decide on their algorithm's behavior.

    def __init__(self, init_map=None):
        """
        Constructor.
        :param init_map: initialization map of pitches to pitches, each either textual or DiatonicPitch
        """

        imap = dict()
        if init_map is not None:
            for key, value in init_map.items():
                if not isinstance(key, DiatonicPitch) and not isinstance(key, str):
                    raise Exception('Key \'{0}\' must be DiatonicPitch or string.'.format(key))
                if isinstance(key, str):
                    key = GeneralPitchFunction._parse_key(key)
                    if key is None:
                        raise Exception('Key \'{0}\' illegal syntax for pitch.'.format(key))

                if value is not None:
                    if not isinstance(value, DiatonicPitch) and not isinstance(value, str):
                        raise Exception('Value \'{0}\' must be DiatonicPitch or string.'.format(value))
                    if isinstance(value, str):
                        value = GeneralPitchFunction._parse_value(value)
                        if value is None:
                            raise Exception('Value \'{0}\' illegal syntax for pitch.'.format(value))

                imap[key] = value

        DiscreteFunction.__init__(self, imap)

    @staticmethod
    def _check_set(df_set):
        if df_set is None:
            return set()
        if not isinstance(df_set, list) and not isinstance(df_set, set):
            raise Exception('Parameter \'{0}\' must be a list or set.'.format(df_set))
        p_set = set()
        for s in df_set:
            if not isinstance(s, DiatonicPitch) and not isinstance(s, str):
                raise Exception('\'{0}\' must be a diatonic pitch or string.'.format(s))
            if isinstance(s, str):
                s = DiatonicPitch.parse(s)
                if s is None:
                    raise Exception('\'{0}\' is not a valid pitch.'.format(s))
            p_set.add(s)
        return p_set

    @staticmethod
    def _parse_key(key):
        if not isinstance(key, DiatonicPitch) and not isinstance(key, str):
            raise Exception('Key value {0} must be a diatonic pitch or string for pitch.'.format(key))
        if isinstance(key, str):
            key = DiatonicPitch.parse(key)
            if key is None:
                raise Exception('Invalid pitch format \'{0}\'.'.format(key))
        return key

    @staticmethod
    def _parse_value(value):
        if not isinstance(value, DiatonicPitch) and not isinstance(value, str):
            raise Exception('Value \'{0}\' must be a diatonic pitch or string.'.format(value))
        if value is None:
            return None
        if isinstance(value, str):
            n_value = DiatonicPitch.parse(value)
            if n_value is None:
                raise Exception('Value \'{0}\' is not a pitch nor \'None\'.'.format(value))
            else:
                value = n_value
        return value

    def __str__(self):
        return '[' + ','.join('({0}-->{1})'.format(key, self[key]) for key in self.domain) + ']'

    def __getitem__(self, key):
        if key is None:
            return None
        if isinstance(key, str):
            key = GeneralPitchFunction._parse_key(key)
            if key is None:
                raise Exception('Key \'{0}\' illegal syntax for pitch.'.format(key))
        elif not isinstance(key, DiatonicPitch):
            raise Exception('Key \'{0}\' must be pitch or string.'.format(key))
        if key not in self.domain:
            raise Exception('Key \'{0}\' not in function domain.'.format(str(key)))
        return super(GeneralPitchFunction, self).__getitem__(key)

    def __setitem__(self, key, value):
        key = GeneralPitchFunction._parse_key(key)
        if key not in self.domain:
            raise Exception('Key \'{0}\' not in function domain.'.format(str(key)))

        n_value = GeneralPitchFunction._parse_value(value) if value is not None else None
        value = n_value if n_value is not None and isinstance(n_value, DiatonicPitch) else value
        if value not in self.range and value is not None:
            raise Exception('Value \'{0}\' not in function range.'.format(str(value)))
        super(GeneralPitchFunction, self).__setitem__(key, value)

    def __delitem__(self, key):
        raise Exception('Delete not an allowed operation.')
