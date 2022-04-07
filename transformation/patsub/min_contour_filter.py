"""

File: min_contour_filter.py

Purpose: To provide a ranking of patsub solutions.

"""


class MinContourFilter(object):
    """
    For a given target pattern, and a set of results, e.g. patsub, based on the target pattern, rank the results
    best to worst.  The metric is as follow:
        A = set of chromatic distances between target pattern note pairs.
        For each instance:
            B = set of chromatic distances between instance notes pairs.
            measure = sum of (A[i] - B[i])**2
        Ranks instances low to high by measure.
    """

    def __init__(self, target_pattern, target_instance_list):
        """
        Constructor.
        :param target_pattern: The given pattern.
        :param target_instance_list:  A set of instances based on the target pattern.
        """
        self.__target_pattern = target_pattern
        self.__target_instance_list = target_instance_list

        self.__scored_results = self._compute_min_results()
        self.__results = [instance[0] for instance in self.__scored_results]

    @property
    def target_pattern(self):
        return self.__target_pattern

    @property
    def target_instance_list(self):
        return self.__target_instance_list

    @property
    def results(self):
        return self.__results

    @property
    def scored_results(self):
        return self.__scored_results

    def _compute_min_results(self):
        pattern_notes = [n for n in self.target_pattern.get_all_notes() if n.diatonic_pitch is not None]
        pattern_diffs = [pattern_notes[i].diatonic_pitch.chromatic_distance -
                         pattern_notes[i - 1].diatonic_pitch.chromatic_distance
                         for i in range(1, len(pattern_notes))]

        instance_results = list()
        for instance in self.target_instance_list:
            instance_notes = MinContourFilter._get_pmap_notes(instance)

            if len(pattern_notes) != len(instance_notes):
                raise Exception('target pattern and instance have different numbers of notes')

            instance_diffs = [instance_notes[i].diatonic_pitch.chromatic_distance -
                              instance_notes[i - 1].diatonic_pitch.chromatic_distance
                              for i in range(1, len(instance_notes))]
            s = sum([(instance_diff - pattern_diff) * (instance_diff - pattern_diff)
                     for instance_diff, pattern_diff in zip(instance_diffs, pattern_diffs)])

            instance_results.append((self.pmap_to_line(instance), s))

        return sorted(instance_results, key=lambda instance_result: instance_result[1])

    @staticmethod
    def _get_pmap_notes(pmap):
        target_notes = [k for k in pmap.keys()]
        target_notes = sorted(target_notes, key=lambda tn: tn.get_absolute_position())
        return [pmap[key].note for key in target_notes]

    def pmap_to_line(self, pmap):
        notes = self._get_pmap_notes(pmap)
        line = self.target_pattern.clone()
        l_notes = line.get_all_notes()
        for note, l_note in zip(notes, l_notes):
            l_note.diatonic_pitch = note.diatonic_pitch
        return line
