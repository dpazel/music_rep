"""

File: p_map.py

Purpose: Wrapper for solver parameter map, that allow a form of replication not found in usual dict structures. 

"""
from collections import OrderedDict

from tonalmodel.pitch_scale import PitchScale
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from melody.constraints.policy_context import PolicyContext
from melody.constraints.contextual_note import ContextualNote
from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from timemodel.duration import Duration


class PMap(object):
    """
    Wrapper for dict based solver parameter map. Class provides adequate replication method that is used in solver
    to collect results.
    The mapping is usually from Note to ContextualNote.
    """

    def __init__(self, p_map=None):
        """
        Constructor
        :param p_map: An OrderedDict, user constructed for the solver.
        """
        self._p_map = OrderedDict() if p_map is None else p_map

    @property
    def p_map(self):
        return self._p_map

    @property
    def actors(self):
        return [actor for actor in self.keys()]

    def keys(self):
        return self._p_map.keys()

    def values(self):
        return self._p_map.values()

    def assigned_actors(self, abstract_policy):
        """
        Return a list of constraints actors that have assigned target notes.
        :param abstract_policy:
        :return:
        """
        return [actor for actor in abstract_policy.actors if self[actor].note is not None]

    def unassigned_actors(self, abstract_policy):
        """
        Return a list of constraints actors that do not have assigned target notes.
        :param abstract_policy:
        :return:
        """
        return [actor for actor in abstract_policy.actors if self[actor].note is None]

    def unassigned(self):
        return [actor for actor in self.keys() if self[actor].note is None]

    def replicate(self):
        """
        Replicate the p_map, based on solver logic, we only replicate the map's target only up to
        the ContextualNote.  The rest is the same.
        :return: 
        """
        p_map = OrderedDict()
        for k in self.p_map.keys():
            p_map[k] = None if k not in self.p_map else self.p_map[k].replicate()
        return PMap(p_map)

    def __getitem__(self, key):
        return self._p_map[key]

    def __contains__(self, key):
        return key in self._p_map

    def __setitem__(self, key, value):
        self._p_map[key] = value

    def __str__(self):
        s = list()
        s.append('=========')
        for k in self.p_map.keys():
            s.append('{0} --> {1}'.format(k.diatonic_pitch,
                                          'None' if self.p_map[k].note is None else self.p_map[k].note.diatonic_pitch))
        s.append('=========')
        return '\n'.join(s)

    def all_tonal_pitches(self, v_note):
        """
        Compute all tonal pitches for the target of a v_note in p_map.
        :param v_note:
        :return:
        """
        target = self[v_note]
        if target is None:
            raise Exception('Internal construction error, v_note target is None.')
        policy_context = target.policy_context
        return PitchScale.compute_tonal_pitches(policy_context.harmonic_context.tonality,
                                                policy_context.pitch_range)

    def apply(self, line, line_copy=True):
        """
        Apply this pmap's mapping to the tones in line or a copy of line.
        :param line:
        :param line_copy:
        :return:
        """
        target_line = line.clone() if line_copy else line
        note_map = dict()
        for line_note, t in zip(line.get_all_notes(), target_line.get_all_notes()):
            note_map[line_note] = t

        for l_note in line.get_all_notes():
            if l_note in note_map:
                t = note_map[l_note]
                if l_note in self.keys():
                    t.diatonic_pitch = self[l_note].note.diatonic_pitch if self[l_note].note is not None \
                        else t.diatonic_pitch

        return target_line

    def _get_pmap_notes(self):
        target_notes = [k for k in self.keys()]
        target_notes = sorted(target_notes, key=lambda tn: tn.get_absolute_position())
        return [self[key].note for key in target_notes]

    def as_line(self):
        from structure.line import Line
        notes = self._get_pmap_notes()
        line = Line(notes).clone()
        return line

    @staticmethod
    def build_hct(hc_expressed_list):
        parse_str = '{'
        for t in hc_expressed_list:
            parse_str += '<' + t[0] + '> qC:4 '
        parse_str += '}'

        lge = LineGrammarExecutor()

        _, hct = lge.parse(parse_str)
        new_hct = HarmonicContextTrack()
        for hc, t in zip(hct.hc_list(), hc_expressed_list):
            duration = t[1] if isinstance(t[1], Duration) else Duration(t[1])
            new_hc = HarmonicContext(hc.tonality, hc.chord, duration)
            new_hct.append(new_hc)
        return new_hct

    @staticmethod
    def create(line_str, pitch_range, target_hct_list=None):
        """
        Create a PMap from
        :param line_str: a melodic string
        :param pitch_range: PitchRange
        :param target_hct_list: list of pairs ('tonality:chord', duration)
        :return: pmap
        Note if target_hct_list is not specified, we use the hct from the line_str.
        """
        lge = LineGrammarExecutor()
        line, hct = lge.parse(line_str)
        if target_hct_list is not None:
            hct = PMap.build_hct(target_hct_list)
        actors = line.get_all_notes()

        d = OrderedDict()
        for note in actors:
            hc = hct[note.get_absolute_position().position]
            if hc is None:
                raise Exception('Cannot locate harmonic context for note \'{0}\''.format(note))
            contextual_note = ContextualNote(PolicyContext(hc, pitch_range))
            d[note] = contextual_note

        return PMap(d)

    def __hash__(self):
        return hash(len(self.actors))

    def __eq__(self, other):
        if not isinstance(other, PMap):
            return NotImplemented
        return self is other
