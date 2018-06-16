"""

File: harmonic_context_track.py

Purpose: Defines a list container for harmonic context indexed by position.

Note: HarmonicContext positions are continually reset when the track is built.  The position of the first HC
      will be 0.

"""
from misc.ordered_map import OrderedMap
from timemodel.position import Position
from timemodel.duration import Duration


class HarmonicContextTrack(object):

    def __init__(self):
        """
        Constructor.
        """
        self.ordered_map = OrderedMap()
        self._wnt_duration = Duration(0)

    def __getitem__(self, position):
        """
        Get the harmonic context based on the floor of the given position.

        :param position:
        :return:
        """
        floor_position = self.ordered_map.floor(position)
        return None if floor_position is None else self.ordered_map[floor_position]

    def __len__(self):
        return len(self.ordered_map)

    @property
    def duration(self):
        return self._wnt_duration

    def hc_list(self):
        return [self.ordered_map[hc] for hc in self.ordered_map.keys()]

    def reset(self):
        self._reset_hc_list(self.ordered_map.value_items())

    def append(self, harmonic_context):
        """
        Append a harmonic context to the end of the track.
        It is recommended to use this call to build the track, as the key data members are not rebuilt.

        :param harmonic_context:
        :return:
        """
        last_hc = None if self.ordered_map.is_empty() else self.ordered_map.value_items()[-1]

        harmonic_context.position = Position(0) if last_hc is None else last_hc.position + last_hc.duration
        self.ordered_map.insert(harmonic_context.position, harmonic_context)

        self._wnt_duration += harmonic_context.duration.duration

    def append_first(self, harmonic_context):
        """
        Append a harmonic context to the beginning of the track, and shove right all existing HC's
        by the duration of the added HC.
        :param harmonic_context:
        :return:
        """
        hc_list = self.ordered_map.value_items()
        hc_list.insert(0, harmonic_context)
        self._reset_hc_list(hc_list)

    def insert(self, position_key, harmonic_context):
        """
        Insert a harmonic context at a given position.  The insertion happens after the HC that is floor(position_key).
        :param position_key:
        :param harmonic_context:
        :return:
        """
        hc_list = self.ordered_map.value_items()
        hc_target_index = self.ordered_map.floor(position_key)
        index = 0 if hc_target_index is None else hc_list.index(self.ordered_map[hc_target_index])
        hc_list.insert(index, harmonic_context)
        harmonic_context.position = position_key
        self._reset_hc_list(hc_list)

    def get_hc_by_position(self, position):
        return self.ordered_map[self.ordered_map.floor(position)]

    def replace(self, position_key, harmonic_context):
        if position_key not in self.ordered_map:
            raise Exception('Attempt to replace a harmonic context with invalid key')
        harmonic_context.position = position_key
        self.ordered_map.insert(position_key, harmonic_context)
        self._reset_hc_list(self.ordered_map.value_items())

    def remove(self, harmonic_context):
        """
        Remove the given harmonic content.  Error if it does not exist.
        :param harmonic_context:
        :return:
        """
        if harmonic_context.position not in self.ordered_map or \
                self.ordered_map[harmonic_context.position] != harmonic_context:
            raise Exception('Attempt of remove harmonic context that is not in list')
        self.ordered_map.remove_key(harmonic_context.position)
        self._reset_hc_list(self.ordered_map.value_items())

    def _reset_hc_list(self, hc_list):
        p = Position(0)
        new_ordered_map = OrderedMap()
        for hc in hc_list:
            hc.position = p
            new_ordered_map.insert(p, hc)
            p += hc.duration
        self.ordered_map = new_ordered_map
        self._wnt_duration = Duration(p.position)

    def clear(self):
        self.ordered_map = OrderedMap()
        self._wnt_duration = Duration(0)

    def __str__(self):
        l = self.hc_list()
        return '\n'.join('[{0}] {1}'.format(i, str(l[i])) for i in range(0, len(self)))
