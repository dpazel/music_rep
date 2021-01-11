from abc import ABC, abstractmethod

from timemodel.duration import Duration
from timemodel.position import Position
from fractions import Fraction


class AbstractMotif(ABC):

    def __init__(self, actors, constraints=list()):
        self.__actors = list(actors)
        self.__constraints = list(constraints)
        self.__position = Position(0)

        self.actor_constraint_map = self._build_actor_constraint_map()

        super().__init__()

    @property
    def duration(self):
        if len(self.__actors) == 0:
            return Duration(0)

        # We assume:
        #   1) That the position of the first note identifies to the start of the motif.
        #   2) That although notes are properly sequential, there could be notes position earlier than the last
        #      whose duration extends past the end of the last note.
        start_position = self.__actors[0].position.position
        answer = Fraction(0)
        for actor in self.__actors:
            answer = Fraction(max(answer, actor.position.position - start_position + actor.duration.duration))
        return Duration(answer)

    @property
    def position(self):
        if len(self.actors) == 0:
            return None
        return self.__actors[0].get_absolute_position()

    @property
    def actors(self):
        return list(self.__actors)

    @property
    def constraints(self):
        return list(self.__constraints)

    @property
    @abstractmethod
    def name(self):
        pass

    def add_constraint(self, constraint):
        if constraint in self.__constraints:
            return
        self.__constraints.append(constraint)
        self.actor_constraint_map = self._build_actor_constraint_map()

    def remove_constraint(self, constraint):
        if constraint not in self.constraints:
            raise Exception('Attempt to remove constraint {0} not in motif {1}'.format(constraint, self.name))
        self.__constraints.remove(constraint)
        self.actor_constraint_map = self._build_actor_constraint_map()

    def constraints_for(self, actor):
        return self.actor_constraint_map[actor] if actor in self.actor_constraint_map else None

    def _build_actor_constraint_map(self):
        element_constraints_map = dict()  # map mote/element to set of constraints in which involved
        for constraint in self.constraints:
            for actor in constraint.actors:
                if actor not in element_constraints_map:
                    element_constraints_map[actor] = list()
                element_constraints_map[actor].append(constraint)
        return element_constraints_map
