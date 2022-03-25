"""

File: policy_context.py

Purpose: Used by pmap to hold the appropriate harmonic context and pitch range.

"""


class PolicyContext(object):

    def __init__(self, harmonic_context, pitch_range):
        self._harmonic_context = harmonic_context
        self._pitch_range = pitch_range

    @property
    def harmonic_context(self):
        return self._harmonic_context

    @property
    def pitch_range(self):
        return self._pitch_range

    def __eq__(self, other):
        if other is None:
            return False
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return 'p.c.[{0}, {1}]'.format(self.harmonic_context, self.pitch_range)
