from function.discrete_function import DiscreteFunction


class Permutation(DiscreteFunction):
    """
    Permutation class. Defines permutation over objects given a well defined domain for the objects, and
    and array of array of obbjects that specify the permutation itself.
    Note: We use right-hand functional behavior, i.e.  p1 * p2[i] = p1(p2[i]).  So, evaluation of 'multiplied'
          permutations is from right to left.
    """

    def __init__(self, p_domain, cycles):
        """
        Create a permutation given:
        :param p_domain: The set of ALL elements that are members of the permutation.
        :param cycles: The permutation itself, an array of array of domain elements.
        """

        Permutation.check_cycles(p_domain, cycles)

        self.__cycles = Permutation.normalize(p_domain, cycles)

        DiscreteFunction.__init__(self, Permutation.generate_init_map(p_domain, self.cycles))

    @property
    def cycles(self):
        return self.__cycles

    def inverse(self):
        # reverse all the cycles
        r_cycles = list()
        for cycle in reversed(self.cycles):
            r_cycle = [x for x in reversed(cycle)]
            r_cycles.append(r_cycle)
        return Permutation(self.domain, r_cycles)

    def __mul__(self, other):   # self on left
        cycles = list(self.cycles)
        cycles.extend(other.cycles)
        return Permutation(self.domain, cycles)

    def __rmul__(self, other):  # self on right
        cycles = list(other.cycles)
        cycles.extend(self.cycles)
        return Permutation(self.domain, cycles)

    @staticmethod
    def check_cycles(domain, cycles):
        if not isinstance(cycles, list):
            raise Exception('Cycles must be a list not {0}.'.format(type(list)))

        for cycle in cycles:
            if not isinstance(cycle, list):
                raise Exception('Cycle must be a list not {0}.'.format(type(list)))
            # all elements in domain?
            not_in_domain = {x for x in cycle if x not in domain}
            if len(not_in_domain) > 0:
                raise Exception('Elements in cycle {0} must be in domain.'.format(cycle))
            # any duplicates?
            seen = set()
            twice_seen = {x for x in cycle if x in seen or seen.add(x)}
            if len(twice_seen) > 0:
                raise Exception('Duplicate elements in cycle {0}.'.format(cycle))

    @staticmethod
    def normalize(domain, cycles):
        seen = set()
        new_cycles = list()
        for v in domain:
            if v in seen:
                continue
            new_cycle = list()
            start = v
            new_cycle.append(v)
            seen.add(v)
            while True:
                v = Permutation.apply(cycles, v)
                if v == start:
                    break
                new_cycle.append(v)
                seen.add(v)

            new_cycles.append(new_cycle)

        return new_cycles

    @staticmethod
    def apply(cycles, x):
        for cycle in cycles[::-1]:
            x = Permutation.apply_cycle(cycle, x)
        return x

    @staticmethod
    def apply_cycle(cycle, x):
        i = cycle.index(x) if x in cycle else None
        if i is None:
            return x
        next_index = i + 1 if i < len(cycle) - 1 else 0
        return cycle[next_index]

    @staticmethod
    def generate_init_map(domain, cycles):
        init_map = dict()
        for x in domain:
            y = Permutation.apply(cycles, x)
            init_map[x] = y

        return init_map

    def __getitem__(self, key):
        return self.apply(self.cycles, key)

    def __setitem__(self, key, value):
        raise Exception('Cannot set elements once a permuation is created.')

    def __delattr__(self, item):
        raise Exception('Cannot delete elements once a permutation is created.')

    def __str__(self):
        tcycles = []
        for c in self.cycles:
            tcycles.append('[{0}]'.format(', '.join(str(x) for x in c)))
        txt = ', '.join(x for x in tcycles)
        return '[{0}]'.format(txt)
