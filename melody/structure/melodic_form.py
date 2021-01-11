"""

File: melodic_motif.py

Purpose: Encapsulates all details of a melody as covered by motifs, forms, and phrases.

"""
import itertools
from melody.structure.form import Form


class MelodicForm(Form):

    def __init__(self, components, phrases=list(), constraints=list(), name=None):
        """
        :param components: A list of Motif's or Forms, positioned sequentially.
        :param phrases:
        :param constraints:
        :param name:
        """

        self.__phrases = list(phrases)
        self.__name = name

        self.__phrase_actors, self.phrase_start_map = Form._all_actors(self.phrases)
        self.__phrase_constraints = list(itertools.chain(sum((p.constraints for p in self.phrases), [])))

        Form.__init__(self, components, constraints)

        all_actors, _ = Form._all_actors(components)
        for constraint in self.phrase_constraints:
            for a in constraint.actors:
                if a not in all_actors:
                    raise Exception('Actor {0} in phrase constraint {1} is not actor in MelodicForm.'.
                                    format(a, constraint))

    @property
    def phrases(self):
        return self.__phrases

    @property
    def phrase_actors(self):
        return self.__phrase_actors

    @property
    def phrase_constraints(self):
        return self.__phrase_constraints

    @property
    def constraints(self):
        return super(MelodicForm, self).constraints + self.phrase_constraints

    def copy_to(self, first_note):
        components = Form._copy_components(self.components, self.actors[0], self.component_start_map, first_note)

        actors, _ = Form._all_actors(components)
        if len(self.actors) != len(actors):
            return None

        note_map = {a: b for a, b in zip(self.actors, actors)}
        copy_constraints = [x.clone([note_map[a] for a in x.actors]) for x in self.external_constraints]

        copy_phrases = Form._copy_components(self.phrases, self.actors[0], self.phrase_start_map, first_note)

        return MelodicForm(components, copy_phrases, copy_constraints, self.name)

    def __str__(self):
        if self.__name is not None:
            return self.__name
        else:
            super(MelodicForm, self).__str__()
