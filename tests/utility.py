TONES = list('CDEFGAB')


def build_offset_list(scale):
    iter_scale = iter(scale)
    first = next(iter_scale)
    base = first.tonal_offset
    last_diff = 0
    tonal_offsets = []
    for dt in iter_scale:
        diff = dt.tonal_offset - base
        if diff < 0:
            diff += 12
        # This is the difference in which we are interested
        delta = diff - last_diff
        # Typically on the last letter, we return to the small value again, and need to 
        # normalize mode 12
        if delta < 0:
            delta += 12
        tonal_offsets.append(delta)
        last_diff = diff 
    return tonal_offsets 


def build_incremental_intervals(scale):
    from tonalmodel.diatonic_pitch import DiatonicPitch
    from tonalmodel.interval import Interval
    partition = 4
    iter_scale = iter(scale)
    first = next(iter_scale)
    prior_pitch = DiatonicPitch(partition, first)
    prior = TONES.index(first.diatonic_letter)
    intervals = [Interval.parse('P:1')]
    for dt in iter_scale:    
        if TONES.index(dt.diatonic_letter) - prior < 0:
            partition += 1
        prior = TONES.index(dt.diatonic_letter)
        current_pitch = DiatonicPitch(partition, dt)
        intervals.append(Interval.create_interval(prior_pitch, current_pitch))
        
        prior_pitch = current_pitch
        
    return intervals    


def build_letter_offset_list(scale):
    iter_scale = iter(scale)
    first = next(iter_scale)
    prior = TONES.index(first.diatonic_letter)
    offsets = []
    for dt in iter_scale:
        offset = TONES.index(dt.diatonic_letter) - prior
        offset = offset if offset >= 0 else offset + 7
        prior = TONES.index(dt.diatonic_letter)

        offsets.append(offset)
    return offsets


def get_symbol(dt):
    return dt.diatonic_symbol
