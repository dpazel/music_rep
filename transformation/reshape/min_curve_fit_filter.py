"""

File: min_curve_fit_filter.py

Purpose: To provide a ranking of patsub solutions.

"""


class MinCurveFitFilter(object):
    """
    For a given target pattern, and a set of results, e.g. patsub, based on the target pattern, rank the results
    best to worst.  The metric is as follow:
        A = set of chromatic distances between target pattern note pairs.
        For each instance:
            B = set of chromatic distances between instance notes pairs.
            measure = sum of (A[i] - B[i])**2
        Ranks instances low to high by measure.
    """

    def __init__(self, pitch_function, target_instance_list):
        """
        Constructor.
        :param pitch_function: GenericUnivariatePitchFunction.
        :param target_instance_list:  A set of instances based on the target pattern.
        """
        self.__pitch_function = pitch_function
        self.__target_instance_list = target_instance_list

        self.__scored_results = self._compute_min_results()
        self.__results = [instance[0] for instance in self.__scored_results]

    @property
    def pitch_function(self):
        return self.__pitch_function

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

        instance_results = list()
        for instance in self.target_instance_list:
            instance_notes = instance.line.get_all_notes()

            instance_diffs = [instance_notes[i].diatonic_pitch.chromatic_distance -
                              self.pitch_function.eval_as_accurate_chromatic_distance(
                                  instance_notes[i].get_absolute_position().position)
                              for i in range(0, len(instance_notes))]
            s = sum([instance_diff * instance_diff for instance_diff in instance_diffs])

            instance_results.append((instance, s))

        return sorted(instance_results, key=lambda instance_result: instance_result[1])
