"""

File: Form.py

Purpose: Encapsulates a note figure composed of a number of motifs, along with their constraints.

"""
import itertools

from melody.structure.abstract_motif import AbstractMotif
from melody.structure.motif import Motif
from melody.structure.phrase import Phrase
from structure.note import Note


class Form(AbstractMotif):

    def __init__(self, components, constraints=list()):
        """
        Constructor
        :param components: A list of Motif's or Forms, positioned sequentially.
        :param constraints: Constraints within or across mentioned motifs
        Note: constraints must specify actors from motifs, for actor belonging to multiple motifs, results are
              unreliable.
        """
        self.__components = components if isinstance(components, list) else [components]
        self.__motifs = Form._all_motifs(self.components)

        self.external_constraints = constraints

        actors, self.component_start_map = Form._all_actors(self.components)
        for constraint in constraints:
            for a in constraint.actors:
                if a not in actors:
                    raise Exception('Actor {0} in constraint {1} not a Form actor.'.format(a, constraint))

        AbstractMotif.__init__(self, actors,
                               list(itertools.chain(sum((m.constraints for m in self.motifs), []), constraints)))

    @property
    def components(self):
        return self.__components

    @property
    def motifs(self):
        return self.__motifs

    @property
    def name(self):
        return str(self)

    def copy_to(self, first_note):
        components = Form._copy_components(self.components, self.actors[0], self.component_start_map, first_note)

        actors, _ = Form._all_actors(components)
        if len(self.actors) != len(actors):
            return None
        note_map = {a: b for a, b in zip(self.actors, actors)}

        copy_constraints = [x.clone([note_map[a] for a in x.actors]) for x in self.external_constraints]

        return Form(components, copy_constraints)

    def reverse(self):
        pass

    def __str__(self):
        return '.'.join([str(motif.name) for motif in self.motifs])

    @staticmethod
    def _all_motifs(components):
        all_motifs = list()
        for component in components:
            if isinstance(component, Motif):
                all_motifs.append(component)
            elif isinstance(component, Form):
                all_motifs.extend(Form._all_motifs([component]))
            else:
                raise Exception('Form component {0} not Motif nor Form'.format(type(component)))

        return sorted(all_motifs, key=lambda x: x.get_absolute_position() if isinstance(x, Note) else x.position)

    @staticmethod
    def _all_actors(components):
        actors = set()
        component_start_map = dict()
        for component in components:
            if isinstance(component, Motif) or isinstance(component, Phrase):
                component_actors = component.actors
            elif isinstance(component, Form):
                component_actors, _ = Form._all_actors([component])
            else:
                raise Exception('Form component {0} not Motif nor Form'.format(type(component)))
            if component_actors[0] not in component_start_map:
                component_start_map[component_actors[0]] = list()
            component_start_map[component_actors[0]].append(component)
            actors = actors.union(set(component_actors))

        actors = list(actors)
        actors = sorted(actors, key=lambda x: x.get_absolute_position())
        return actors, component_start_map

    @staticmethod
    def _copy_components(s_components, s_note, resource_note_map, first_note):
        components = []
        seen = set()
        source_note = s_note
        n = first_note
        while True:
            s_component_list = resource_note_map[source_note] if source_note in resource_note_map else None
            if s_component_list is not None:
                for s_component in s_component_list:
                    if s_component in seen:
                        continue
                    component = s_component.copy_to(n)
                    components.append(component)
                    seen.add(s_component)
                if len(s_components) == len(components):
                    break
            source_note = source_note.next_note()
            n = n.next_note()

        return components
