"""

File: pitch_constraint_solver.py

Purpose: For a melody define as a p_map, and a set of policy constraints, solve for compatible melodies
         satisfying constraints, as a set of p_map's.

"""
from melody.solver.p_map import PMap
from structure.note import Note


class PitchConstraintSolver(object):
    """
    Implementation class for a constraint solver that attempts to find pitch solutions to pitch constraints.
    """

    def __init__(self, policies):
        """
        Constructor.

        :param policies: non-null set of policies
        """
        if policies is None or (not isinstance(policies, set) and not isinstance(policies, list)):
            raise Exception('Policies must be non-null and a Set')

        self._policies = set(policies)

        self.v_policy_map = dict()
        self._build_v_policy_map()

        self.__instance_limit = 0
        self.__num_instances = 0
        self.__full_results = list()

    @property
    def policies(self):
        return [p for p in self._policies]

    @property
    def num_instances(self):
        return self.__num_instances

    @property
    def instance_limit(self):
        return self.__instance_limit

    @property
    def full_results(self):
        return self.__full_results

    def solve(self, p_map_param, instance_limit=-1, accept_partials=False):
        """
        Solve the constraints constraint system using p_map_param as the start.
        :param p_map_param:  Initial PMap to fill out.
        :param instance_limit: Number of full results to limit search; -1 no limit
        :param accept_partials: Boolean, True means return some partial results
        :return:
        """
        p_map = p_map_param if isinstance(p_map_param, PMap) else PMap(p_map_param)
        self._check_p_map(p_map)

        self.__instance_limit = instance_limit
        self.__num_instances = 0  # reset
        self.__full_results = list()

        partial_results = [p_map]
        # list of tuples (v_note, {solution to v_note's policies})
        unsolved_nodes = [t[0] for t in self._build_potential_values(p_map, p_map.keys())]
        if len(unsolved_nodes) == 0:
            raise Exception('Policies insufficient for solution or parameter map is full.')

        while len(unsolved_nodes) != 0:
            v_note = unsolved_nodes[0]
            results_prime = list()
            for p_map in partial_results:
                if p_map[v_note] is None or p_map[v_note].note is None:
                    visit_results = self.__fill_chain(p_map, v_note)
                    if len(visit_results) == 0:
                        if accept_partials:   # if accept partials, keep in partial results.
                            results_prime.append(p_map)
                    else:
                        results_prime.extend(visit_results)   # note: contains possible extensions of pmap
                else:  # v_note already filled, keep it in partial_results.
                    results_prime.append(p_map)
            partial_results = results_prime
            if self.instance_limit != -1 and len(partial_results) >= self.instance_limit:
                break
            unsolved_nodes.remove(v_note)
            peer_notes = self._candidate_closure(p_map, v_note)
            for n in peer_notes:
                if n in unsolved_nodes:
                    unsolved_nodes.remove(n)

        return self.full_results, partial_results if accept_partials else list()

    def _check_p_map(self, p_map):
        if self.v_policy_map.keys() != p_map.keys():
            raise Exception('PMap keys and policy actor keys do not match.')

    @staticmethod
    def pmap_full(p_map):
        v = [p_map[key].note for key in p_map.keys()]
        if None in v:
            return False
        return True
        # return len([v_note for v_note in p_map.keys() if p_map[v_note].note is None]) == 0

    def __fill_chain(self, p_map, v_note):
        return_results = set()
        result_values = self._build_potential_values(p_map, {v_note})
        if len(result_values) == 0:
            return return_results
        v_note_values = result_values[0][1]

        peer_notes = self._candidate_closure(p_map, v_note)
        peer_notes.remove(v_note)
        num_left_unassigned = len(p_map.unassigned()) - len(peer_notes) - 1

        for value in v_note_values:
            p_map[v_note].note = value
            v_note_p_map_set = {p_map.replicate()}

            for peer in peer_notes:
                peer_p_map_results = set()  # For this peer, all p_maps for this v_note setting and all prior looped peer settings.
                                            # A set that contains p_pmaps which progressively peer settings. v_note_p_map_set get replaced by it per peer loop
                peer_p_map_value_results = self._build_potential_values(p_map, {peer})
                peer_p_map_values = peer_p_map_value_results[0][1] if len(peer_p_map_value_results) != 0 else set()
                if len(peer_p_map_values) == 0:  # means we advanced to a peer with no values!!! this chain fails for this v_note value
                    v_note_p_map_set = set()
                    break
                for p_map_s in v_note_p_map_set:
                    for p_map_v_note_value in peer_p_map_values:
                        p_map_s[peer].note = p_map_v_note_value

                        if num_left_unassigned == 0 and self._full_check_and_validate(p_map_s):
                            if self.instance_limit != -1 and self.__num_instances >= self.instance_limit:
                                return return_results
                            self.full_results.append(p_map_s.replicate())
                            self.__num_instances = self.__num_instances + 1
                        else:
                            peer_p_map_results.add(p_map_s.replicate())  # We only need a shallow copy
                        p_map_s[peer].note = None
                v_note_p_map_set = peer_p_map_results  # reset the v_note_p_map_set to that having advance another peer setting
            return_results = return_results.union(v_note_p_map_set)  # all peers have been set for this v_note value.

        p_map[v_note].note = None
        return return_results

    def solve_all(self, p_map_param, instance_limit=-1, accept_partials=False):
        p_map = p_map_param if isinstance(p_map_param, PMap) else PMap(p_map_param)
        self._check_p_map(p_map)

        self.__instance_limit = instance_limit
        self.__num_instances = 0  # reset
        self.__full_results = list()

        partial_results = list()
        # list of tuples (v_note, {solution to v_note's policies})
        unsolved_nodes = [t[0] for t in self._build_potential_values(p_map, p_map.keys())]
        if len(unsolved_nodes) == 0:
            raise Exception('Policies insufficient for solution or parameter map is full.')

        node_stack = Stack(unsolved_nodes)
        value_map = ValueMap()
        node = node_stack.next()
        while node is not None:
            if node in value_map:
                values = value_map[node]
            else:
                peer_p_map_value_results = self._build_potential_values(p_map, {node})
                values = peer_p_map_value_results[0][1] if len(peer_p_map_value_results) != 0 else None
                if values is None:
                    partial_results.append(p_map.replicate())
                    value_map.remove(node)
                    node = node_stack.prev()
                    continue

                value_map[node] = values
                values = value_map[node]

            v = values.next()
            if v is None:
                value_map.remove(node)
                p_map[node].note = None
                node = node_stack.prev()
            else:
                p_map[node].note = v
                if self._full_check_and_validate(p_map):
                    if self.instance_limit != -1 and self.__num_instances >= self.instance_limit:
                        return partial_results
                    self.full_results.append(p_map.replicate())
                    print("Append")
                    self.__num_instances = self.__num_instances + 1
                else:
                    node = node_stack.next()

        return self.full_results, partial_results if accept_partials else list()

    def _build_v_policy_map(self):
        for p in self.policies:
            for v_note in p.actors:
                if v_note not in self.v_policy_map:
                    self.v_policy_map[v_note] = []
                self.v_policy_map[v_note].append(p)

    def _build_potential_values(self, p_map, v_notes):
        """
        Compute a list of tuples (v_note, {solution to v_note's policies}), the list being sorted by the number of
        solution values.

        :param p_map: PMap
        :param v_notes: list/set of ContextualNote sources to PMap
        :return: list of tuples (v_note, {solution to v_note's policies})
        """
        ranked_list = list()   # A list of tuples (v_note, {solution values})
        for v_note in v_notes:
            if p_map[v_note] is not None and p_map[v_note].note is not None:
                continue
            values = self._policy_values(p_map, v_note)
            if len(values) == 0:
                continue
            ranked_list.append((v_note, values))

        ranked_list = sorted(ranked_list, key=lambda x: len(x[1]))
        return ranked_list

    def _policy_values(self, p_map, v_note):
        """
        For v_note, find all note values for its target that satisfy all policies in which v_note is involved.
        :param p_map: PMap
        :param v_note: ContextualNote
        :return: A set of notes with same duration as v_note, varying in pitch.
        """
        pitches = None
        for p in self.v_policy_map[v_note]:
            p_values = p.values(p_map, v_note)
            if p_values is None:
                returned_pitches = set()   # None means p cannot be satisfied!
            else:
                returned_pitches = {n.diatonic_pitch for n in p_values}
            pitches = returned_pitches if pitches is None else pitches.intersection(returned_pitches)

        return {Note(p, v_note.base_duration, v_note.num_dots) for p in pitches}

    def _candidate_closure(self, p_map, v_note):
        """
        Find all policies that have v_note as a parameter, and collect their unassigned actors into a set
        without replication.
        :param p_map: PMap
        :param v_note: ContextualNote
        :return:
        """
        policies = self.v_policy_map[v_note]
        candidates = set()
        for p in policies:
            candidates = candidates.union(p_map.unassigned_actors(p))
        return candidates

    def _full_check_and_validate(self, p_map):
        """
        Check if p_map parameter is full and if so, satisfies all policies.
        :param p_map: p_map to be checked
        :return:
        """
        if PitchConstraintSolver.pmap_full(p_map):
            for p in self._policies:
                if not p.verify(p_map):
                    return False
            return True
        else:
            return False


    @staticmethod
    def print_starting_nodes(starting_nodes):

        lst = list()
        for t in starting_nodes:
            s = t[1]
            s_text = '[]' if len(s) == 0 else ', '.join('{0}'.format(n.diatonic_pitch) for n in s)
            full_text = '{0} <== {1}'.format(t[0], s_text)
            lst.append((t[0], full_text))

        ss = sorted(lst, key=lambda x: x[0].get_absolute_position())

        for i in range(0, len(ss)):
            s = ss[i]
            print('[{0}] {1}'.format(i, s[1]))

class Stack(object):

    def __init__(self, objects):
        self.__members = list()
        if isinstance(objects, set):
            self.__members = list(objects)
        elif isinstance(objects, list):
            self.__members.extend(objects)
        else:
            raise Exception("objects must be set or list.")

        self.__index = -1

    def __len__(self):
        return len(self.__members)

    def index(self):
        return self.__index

    def next(self):
        self.__index = self.__index + 1
        if self.__index >= len(self):
            self.__index = -1
        return self.__members[self.__index] if self.__index != -1 else None

    def prev(self):
        self.__index = self.__index - 1
        if self.__index < 0:
            self.__index = -1
        return self.__members[self.__index] if self.__index != -1 else None

class ValueMap(object):
    def __init__(self):
        self.__member_map = dict()
        self.__index = -1

    def __contains__(self, key):
        return key in self.__member_map.keys()

    def __getitem__(self, item):
        if not item in self:
            return None
        return self.__member_map[item]

    def __setitem__(self, key, values):
        self.__member_map[key] = Stack(values)

    def __len__(self):
        return len(self.__member_map)

    def remove(self, key):
        if key in self:
            del self.__member_map[key]


    '''
    Suppose we have a set of non-essential constraints.
    
    Start by solving on the essential ones.
    Then:
        For each c in non-essentials.
           p_map = PMap()
           pick a v_note in c.actors and get its set of solutions
           for each result in solutions:
              p_map[v_note] = value
              for each peer in c.actor not v_note:
                 solve for peer's values
                 recurse this process until all peer's are met.
            This give a set of pmaps that solve c
            cmap[c] = pmaps
            
        Sort this map by len(pmaps) least to highest.
       
       
       For each pmap in essential pmaps:
          for each c in non-essential ordered by low #pmaps
             for each p in cmap[c]:
                 pmap = pmap 'ored' p 
              recurse on this process until you meet some threshold on the solution set size.
    '''

