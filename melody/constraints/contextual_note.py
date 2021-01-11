"""

File: contextual_note.py

Purpose: Define ContextualNote, which is the main data object used in policy management.  It identifies a note
         and the policy context attached to that note.

"""


class ContextualNote(object):
    """
    Class for a contextual wrapper over a note - the wrapper being a constraints context that applies to that note.
    """
    def __init__(self, policy_context, note=None):
        """
        Constructor.
        :param policy_context: PolicyContext
        :param note: Note
        Note: note can be None, which is the case when a constraints.apply() calculates a note, based on, amongst other
              things, the context of the note.
        """
        self._policy_context = policy_context
        self._note = note

    @property
    def policy_context(self):
        return self._policy_context

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, new_note):
        self._note = new_note

    def replicate(self):
        """
        Does a shallow copy of ContextuaNote. We have this over __copy__() out of respect for the emerging logic 
        behind the solver, and provides us leverage in altering this later, as needed. 
        :return: 
        """
        return ContextualNote(self.policy_context, self.note)

    def __str__(self):
        return 'c.n[{0}, {1}]'.format(self.note, self.policy_context)
