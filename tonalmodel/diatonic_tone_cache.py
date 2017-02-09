"""
File: diatonic_tone_cache.py

Purpose: To provide a cachse for DiatonicTone instances.

"""
from tonalmodel.diatonic_tone import DiatonicTone


class DiatonicToneCache(object):
    """"
    Cache for all possible DiatonicTone's.  This cache is very small, but also provides an object level identity
    to each tone in the system, if used.
    The cache is implemented as a singleton.  The constructor is meant to be 'private', and not called externally.
    All access should be through either get_cache() or get_tone().
    """

    DIATONIC_CACHE = None

    def __init__(self):
        """
        Constructor.
        
        Args: None
          
        """
        
        #  map tone name to tone.
        self.diatonic_map = {}
        
        self.__build_diatonics()
        
    @staticmethod
    def get_cache():
        if DiatonicToneCache.DIATONIC_CACHE is None:
            DiatonicToneCache.DIATONIC_CACHE = DiatonicToneCache()
        return DiatonicToneCache.DIATONIC_CACHE

    @staticmethod        
    def get_tone(tone_text):
        cache = DiatonicToneCache.get_cache()
        return cache.get_cache_tone(tone_text)
    
    @staticmethod
    def get_tones():
        cache = DiatonicToneCache.get_cache()
        tones = []
        for ltr in DiatonicTone.DIATONIC_LETTERS:
            for aug in DiatonicTone.AUGMENTATIONS:
                tones.append(cache.get_cache_tone(ltr + aug))
        return tones
    
    def get_cache_tone(self, tone_text):            
        return self.diatonic_map[tone_text.lower()]           

    def __build_diatonics(self):
        """
        Builds all diatonic tones for the cache.
        """
        for ltr in DiatonicTone.DIATONIC_LETTERS:
            for aug in DiatonicTone.AUGMENTATIONS:
                self.diatonic_map[(ltr + aug).lower()] = DiatonicTone(ltr + aug) 