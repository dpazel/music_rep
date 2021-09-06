from melody.structure.abstract_motif import AbstractMotif
from structure.line import Line
from structure.note import Note


class Phrase(AbstractMotif):

    def __init__(self, actors, constraints, name):
        '''

        :param actors: actors (notes) involved in phrase
        :param constraints: constraints on actors
        :param name:
        '''
        self.__name = name
        AbstractMotif.__init__(self, actors, constraints)

    @property
    def name(self):
        return self.__name

    def copy_to(self, first_note):
        new_actors = list()
        n = first_note
        for s in self.actors:
            if n is None:
                return None
            if isinstance(s, Note) and s.duration == n.duration and isinstance(n.parent, Line):
                new_actors.append(n)
                n = n.next_note()
            else:  # Assume s is a structure
                return None

        note_map = {a: b for a, b in zip(self.actors, new_actors)}

        copy_constraints = [x.clone([note_map[a] for a in x.actors]) for x in self.constraints]

        return Phrase(new_actors, copy_constraints, self.name)

    def __str__(self):
        return '.'.join([str(m) for m in self.actors])