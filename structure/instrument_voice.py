"""

File: instrument_voice.py

Purpose: A collection of Voices, each associated with the same instrument.

"""
from voice import Voice
from timemodel.duration import Duration


class InstrumentVoice(object):
    """
    A collection of Voices, each associated with the same instrument.
    """

    def __init__(self, instrument, num_voices=1):
        """
        Constructor.
        The InstrumentVoice retains the instrument, and creates a number of voice, number as specified in
        the constructor.  Each voice uses that instrument.

        Args:
            instrument: Instrument for the voice
            num_voices: Number of voices for this instrument.
        """
        
        self.__instrument = instrument
        self.__voices = [Voice(self.__instrument) for _ in range(num_voices)]
               
    @property
    def instrument(self):
        return self.__instrument
    
    @property
    def voices(self):
        return self.__voices
    
    @property
    def num_voices(self):
        return len(self.__voices)
    
    def voice(self, index):
        if index < 0 or index >= len(self.voices):
            raise Exception('Voice index {0} not in range [{1} -{2})'.format(index, 0, len(self.voices)))
        return self.voices[index]
    
    def get_notes_by_interval(self, interval):
        result = {}
        for i in range(0, self.num_voices):
            notes = self.voice(i).get_notes_by_interval(interval)
            result[self.voice(i)] = notes
        return result
    
    def get_notes_starting_in_interval(self, interval):
        result = {}
        for i in range(0, self.num_voices):
            notes = self.voice(i).get_notes_starting_in_interval(interval)
            result[self.voice(i)] = notes
        return result
    
    def get_all_notes(self):
        result = {}
        for i in range(0, self.num_voices):
            notes = self.voice(i).get_all_notes()
            result[self.voice(i)] = notes
        return result        
    
    @property
    def duration(self):
        return self.length()      
    
    def length(self):
        maxx = Duration(0, 1)
        for voice in self.__voices:
            d = voice.duration
            if d > maxx:
                maxx = d               
        return maxx  
    
    def __str__(self):
        return 'IV[{0}, {1}]'.format(self.instrument, self.num_voices)
