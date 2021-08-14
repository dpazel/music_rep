"""

File: pitch_constraint_solver.py

Purpose: For a melody define as a p_map, and a set of policy constraints, solve for compatible melodies 
         satisfying constraints, as a set of p_map's.

"""
from melody.solver.p_map import PMap
from structure.note import Note
from misc.ordered_set import OrderedSet


class PitchConstraintSolver(object):
    """
    Implementation class for a constraint solver that attempts to find pitch solutions to pitch constraints.
    """

    def __init__(self, policies):
        """
        Constructor.
        
        :param policies: non-null set of policies
        """
        if policies is None or (not isinstance(policies, set) and not isinstance(policies, list) and \
                                not isinstance(policies, OrderedSet)):
            raise Exception('Policies must be non-null and a Set')

        self._policies = OrderedSet(policies)    #set(policies)

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
        # list of tuples (v_note, {solution to v_note's policies}) sorted by low number of solutions.
        unsolved_nodes = [t[0] for t in self._build_potential_values(p_map, p_map.keys())]
        if len(unsolved_nodes) == 0:
            raise Exception('Policies insufficient for solution or parameter map is full.')

        while len(unsolved_nodes) != 0:
            v_node = unsolved_nodes[0]
            results_prime = list()
            for p_map in partial_results:
                if p_map[v_node] is None or p_map[v_node].note is None:
                    visit_results = self._visit(p_map, v_node)
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
            unsolved_nodes.remove(v_node)

        return self.full_results, partial_results if accept_partials else list()

    def _check_p_map(self, p_map):
        for key in self.v_policy_map.keys():
            if key not in p_map.keys():
                raise Exception('PMap keys and policy actor keys do not match.')
        # if self.v_policy_map.keys() != p_map.keys():
        #    raise Exception('PMap keys and policy actor keys do not match.')

    @staticmethod
    def pmap_full(p_map):
        v = [p_map[key].note for key in p_map.keys()]
        if None in v:
            return False
        return True
        # return len([v_note for v_note in p_map.keys() if p_map[v_note].note is None]) == 0

    def _visit(self, p_map, v_note):
        """
        Recursive method used to derive sets of solution to the constraints constraint problem.

        :param p_map: PMap
        :param v_note: ContextualNote, source key of PMap
        :return: A set of pmaps
        """

        if p_map[v_note].note is not None:  # setting means visited
            return {}

        results = OrderedSet()

        # list of tuples (v_note, {solution to v_note's policies})
        result_values = self._build_potential_values(p_map, {v_note})
        if len(result_values) == 0:
            return results

        for value in result_values[0][1]:  # [0] is for v_note; [1] is the set of values.
            p_map[v_note].note = value
            value_results = OrderedSet()  # results for this value for v_note + solutions for ALL peers to v_note

            # Advantage in the following, setting above partially solves each policy v_note is involved in.
            # For this 'value' for v_note, dive depth first through all v_note peers (all policies v_note is in)
            #    which collectively we call a branch.
            # peer_candidates are all unassigned actors in v_note's policies.
            peer_candidates = self._candidate_closure(p_map, v_note)
            if len(peer_candidates) == 0:

                # We reached the end of a branch, save the result.
                if self._full_check_and_validate(p_map):
                    if self.instance_limit != -1 and self.__num_instances >= self.instance_limit:
                        return results
                    self.full_results.append(p_map.replicate())
                    self.__num_instances = self.__num_instances + 1
                else:
                    value_results.add(p_map.replicate())  # We only need a shallow copy

            else:
                for c_note in peer_candidates:
                    if self.instance_limit != -1 and self.__num_instances >= self.instance_limit:
                        results = results.union(value_results)
                        return results

                    if len(value_results) == 0:  # first time through this loop per value, visit with p_map!
                        value_results = self._visit(p_map, c_note)
                        if len(value_results) == 0:  # Indicates failure to assign c_note, move to next value.
                            break                    # If one peer fails, they all will, for this 'value'!
                    else:
                        value_results_copy = value_results.copy()
                        # for peer c_note, if all r below fails (len(cand_results) == 0) should we also move on to
                        # next value? Add 'found' flag, set after union, after loop, check if False, to break
                        found = False
                        for r in value_results_copy:
                            if r[c_note].note is None:
                                cand_results = self._visit(r, c_note)
                                if len(cand_results) != 0:
                                    value_results = value_results.union(cand_results)
                                    found = True
                                value_results.remove(r)  # r has no c_note assigned, what was returned did!
                                                         # If not, r's peers cannot be assigned!
                        if found is False:  # Same as if part, if c_note produces no results, it cannot be assigned.
                            break           # If one peer fails, they all will!
            results = results.union(value_results)

        p_map[v_note].note = None
        return results

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
            if v_note not in self.v_policy_map.keys():
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
                returned_pitches = OrderedSet()    # None means p cannot be satisfied!
            else:
                returned_pitches = OrderedSet()
                for n in p_values:
                    returned_pitches.add(n.diatonic_pitch)
                #returned_pitches = {n.diatonic_pitch for n in p_values}
            pitches = returned_pitches if pitches is None else pitches.intersection(returned_pitches)


        retset = OrderedSet()
        for p in pitches:
            retset.add(Note(p, v_note.base_duration, v_note.num_dots))
        return retset
        #return {Note(p, v_note.base_duration, v_note.num_dots) for p in pitches}

    def _candidate_closure(self, p_map, v_note):
        """
        Find all policies that have v_note as a parameter, and collect their unassigned actors into a set
        without replication.
        :param p_map: PMap
        :param v_note: ContextualNote
        :return: 
        """
        policies = self.v_policy_map[v_note]
        candidates = OrderedSet()
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

    def solve1(self, p_map_param, accept_partials=False, instance_limit=-1):
        """
        Solve the constraints constraint system using p_map as the start.
        :param p_map_param:
        :param accept_partials:
        :param instance_limit:
        :return:
        """
        p_map = p_map_param if isinstance(p_map_param, PMap) else PMap(p_map_param)
        self._check_p_map(p_map)

        self.__instance_limit = instance_limit
        self.__num_instances = 0  # reset

        results = [p_map]
        # list of tuples (v_note, {solution to v_note's policies})
        starting_nodes_prime = self._build_potential_values(p_map, p_map.keys())
        # PitchConstraintSolver.print_starting_nodes(starting_nodes_prime)
        if len(starting_nodes_prime) == 0:
            raise Exception('Insufficient initial information for solution')
        starting_nodes = list()      # list of tuples (v_note, {solution to v_note's policies})

        has_failures = False
        while {a[0] for a in starting_nodes_prime} != {a[0] for a in starting_nodes} and len(starting_nodes_prime) != 0:
            starting_nodes = starting_nodes_prime
            results_prime = list()
            for p_map in results:
                results_prime.extend(self._visit(p_map, starting_nodes[0][0]))
            results = results_prime
            if len(results) == 0:
                has_failures = True
                break
            # TODO: This is an issue when has_failures is True and so results is empty.
            #       Idea: remove starting_nodes[0][0] and use next, and if values set is empty, drop out?
            starting_nodes_prime = self._build_potential_values(results[0], results[0].keys())

        if has_failures:
            return results if accept_partials else list()

        return results

    def _visit_old(self, p_map, v_note):
        """
        Recursive method used to derive sets of solution to the constraints constraint problem.

        :param p_map: PMap
        :param v_note: ContextualNote, source key of PMap
        :return: A set of pmaps
        """
        # print 'Entering Visit vnote={0}'.format(v_note.note.diatonic_pitch)
        # print '   pmap = {0}'.format(p_map)

        if p_map[v_note].note is not None:  # setting means visited
            return {}

        results = set()

        result_values = self._build_potential_values(p_map, {v_note})
        if len(result_values) == 0:
            p_map[v_note].note = None
            return results

        for value in result_values[0][1]:
            value_results = set()  # results for this value for v_note + solutions for all peers to v_mote
            p_map[v_note].note = value

            # Advantage in following peers as above setting partially solves each policy v_note is involved in.
            peer_candidates = self._candidate_closure(p_map, v_note)
            if len(peer_candidates) == 0:
                pmap_full = PitchConstraintSolver.pmap_full(p_map)
                if pmap_full and self.instance_limit != -1 and self.__num_instances >= self.instance_limit:
                    results = results.union(value_results)
                    return results

                # We reached the end of a branch, save the result.
                value_results.add(p_map.replicate())  # We only need a shallow copy
                if pmap_full:
                    self.__num_instances = self.__num_instances + 1

            else:
                for c_note in peer_candidates:
                    if len(value_results) == 0:  # first time through, visit with p_map!
                        value_results = self._visit(p_map, c_note)
                        if len(value_results) == 0:  # Indicates failure to assign c_note, move to next value.
                            break                    # If one peer fails, they all will!
                    else:
                        if self.instance_limit != -1 and self.__num_instances >= self.instance_limit:
                            results = results.union(value_results)
                            return results
                        value_results_copy = value_results.copy()
                        # for peer c_note, if all r below fails (len(cand_results) == 0) should we also move on to
                        # next value? Add 'found' flag, set after union, after loop, check if False, to break
                        found = False
                        for r in value_results_copy:
                            if r[c_note].note is None:
                                cand_results = self._visit(r, c_note)
                                if len(cand_results) != 0:
                                    value_results = value_results.union(cand_results)
                                    found = True
                                value_results.remove(r)
                        if found is False:  # Same as if part, if c_note produces not results, it cannot be assigned.
                            break           # If one peer fails, they all will!
            results = results.union(value_results)

        p_map[v_note].note = None
        return results
