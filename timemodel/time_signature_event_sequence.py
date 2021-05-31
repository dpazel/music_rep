from timemodel.event_sequence import EventSequence

class TimeSignatureEventSequence(EventSequence):
    """
    An event sequence specialized to tempo events.
    """

    def __init__(self, event_list=None):
        """
        Constructor.

        Args:
            event_list: TempoEvents to initialize the sequence.
        """
        EventSequence.__init__(self, event_list)

    def time_signature(self, position):
        tfe = self.floor_event(position)
        return tfe.tempo()
