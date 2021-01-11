"""

File: motif.py

Purpose: Encapsulates a motif note figure plus all constraints proper to that motif, i.e. the constraint actors are
         all from the note figure.

"""
from melody.structure.abstract_motif import AbstractMotif
from structure.abstract_note_collective import AbstractNoteCollective
from structure.line import Line
from structure.note import Note


class Motif(AbstractMotif):

    def __init__(self, note_structure, constraints=list(), name=''):
        """
        Constructor.
        :param note_structure: AbstractNoteCollective, Note, or list of either.
        :param constraints:  list of constraints on notes from above.
        :param name: name of motif
        :return:

        # How about beat and meter specification?
        # Check that each structure is top coverage, i.e. parent is line or line.parent == None
        """

        # Normalize all structure info as a list of note structures and notes.
        structure = note_structure if isinstance(note_structure, list) else [note_structure]
        actors = Motif._extract_actors(structure)
        self.__note_structure = structure

        self.__name = name
        self.__constraints = list(constraints)

        AbstractMotif.__init__(self, actors, constraints)

        # Check that all the constraints' actors list amongst the Motif's actors
        motif_actors = self.actors
        for constraint in self.constraints:
            for a in constraint.actors:
                if a not in motif_actors:
                    raise Exception('Actor {0} in constraint {1} not a Motif actor.'.format(a, constraint))

    @property
    def name(self):
        return self.__name

    @property
    def note_structure(self):
        return self.__note_structure

    def copy_with(self, note_structure):
        """
        Clone the Motif, but using a different note_structure that must structurally match this motif.  This is how
        Motif reuse is achieved in melodic analysis.

        :param note_structure: Note, List of structures, or note structure.
        :return:
        """
        # Do we need to match on note_structural levels???

        new_structure = note_structure if isinstance(note_structure, list) else [note_structure]
        if len(new_structure) != len(self.note_structure):
            return None

        # Check that the actors match 1-1 in duration
        for a, b in zip(self.note_structure, note_structure):
            if isinstance(a, AbstractNoteCollective) == isinstance(b, AbstractNoteCollective):
                if not Motif.__structurally_equal(self.note_structure, note_structure):
                    return None
            elif isinstance(a, Note) == isinstance(b, Note):
                if a.duration != b.duration:
                    return None

        actors = Motif._extract_actors(new_structure)

        note_map = {a: b for a, b in zip(self.actors, actors)}

        copy_constraints = [x.clone([note_map[a] for a in x.actors]) for x in self.constraints]

        return Motif(new_structure, copy_constraints, self.name)

    def copy_to(self, first_note):
        new_structure = list()
        n = first_note
        for s in self.note_structure:
            if n is None:
                return None
            if isinstance(s, Note) and s.duration == n.duration and (n.parent is None or isinstance(n.parent, Line)):
                new_structure.append(n)
                n = n.next_note()
            else:  # Assume s is a structure
                n_level = None
                for s_note in s.get_all_notes():
                    s_level = s_note
                    n_level = n
                    while True:
                        if n_level is None or type(s_level) != type(n_level):
                            return None
                        if s_level == s:
                            break
                        s_level = s_level.parent
                        n_level = n_level.parent
                    n = n.next_note()
                new_structure.append(n_level)

        actors = Motif._extract_actors(new_structure)

        note_map = {a: b for a, b in zip(self.actors, actors)}

        copy_constraints = [x.clone([note_map[a] for a in x.actors]) for x in self.constraints]

        return Motif(new_structure, copy_constraints, self.name)

    @staticmethod
    def __structurally_equal(a, b):
        if type(a) == type(b):
            if isinstance(a, Note) and a.duration == b.duration:
                return True
            if len(a.sub_notes) == len(b.sub_notes):
                for a1, b1 in zip(a.sub_notes, b.sub_notes):
                    if not Motif.__structurally_equal(a1, b1):
                        return False
                return True
            else:
                return False
        else:
            return False

    def reverse(self):
        pass

    def __str__(self):
        strs = ',\n'.join(str(s) for s in self.note_structure)
        return 'Motif[{0}{1}]'.format(self.name + '.' if len(self.name) != 0 else '', strs)

    @staticmethod
    def _extract_actors(note_structure):
        actors = list()
        for n in note_structure:
            if isinstance(n, AbstractNoteCollective):
                actors.extend(n.get_all_notes())
            elif isinstance(n, Note):
                actors.append(n)
            else:
                raise Exception('Motif does not accept type \'{0}\''.format(type(n)))

        return actors
