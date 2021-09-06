"""

File: abstract_constraint.py

Purpose: Define a constraint, in an abstract sense, related to a number of actors.

"""
from abc import ABCMeta, abstractmethod


class AbstractConstraint(object):
    """
    Class that represents a constraint, a set of actors that define a constraint amongst themselves.

    ParameterMap:  A map from template note to contextual note..
    """

    __metaclass__ = ABCMeta

    def __init__(self, actors):
        self.__actors = list(actors)

    @property
    def actors(self):
        return list(self.__actors)

    @abstractmethod
    def clone(self, new_actors=None):
        """
        Clone the constraint.
        :return:
        """

    @abstractmethod
    def verify(self, solution_context):
        """
         Verify that the actor map parameters are consistent with constraint.
         :params solution_context:  aka pmap, map of actors to ContextualNotes.
         :return: Boolean if verification holds.
         May throw Exception dependent on implementation.
         """

    @abstractmethod
    def values(self, solution_context, v_note):
        """
        Method to generate all possible note values for actor v_note's target.
        The method returns a set of values for v_note.
        :param solution_context: includes parameter map.
        :param v_note: source actor, whose target values we are computing.
        :return: The set of all possible values for v_note's target.
        Note: The return value is a set!
        """

    def __hash__(self):
        return hash(len(self.actors))

    def __eq__(self, other):
        if not isinstance(other, AbstractConstraint):
            return NotImplemented
        return self is other

    def actors_by_position(self):
        return sorted(self.actors, key=lambda actor: actor.get_absolute_position())