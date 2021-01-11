from function.function_pitch_range import FunctionPitchRange
from function.piecewise_linear_function import PiecewiseLinearFunction
from tonalmodel.diatonic_pitch import DiatonicPitch


class PiecewiseLinearPitchFunction(PiecewiseLinearFunction, FunctionPitchRange):

    def __init__(self, transition_points=list(), restrict_domain=False):
        tp = PiecewiseLinearPitchFunction._translate_transition_points(transition_points)

        PiecewiseLinearFunction.__init__(self, tp, restrict_domain)
        FunctionPitchRange.__init__(self, self)

    @staticmethod
    def _translate_transition_points(transition_points):
        tps = list()

        for tp in transition_points:
            if isinstance(tp[1], str):
                diatonic_pitch = DiatonicPitch.parse(tp[1])
            elif isinstance(tp[1], DiatonicPitch):
                diatonic_pitch = tp[1]
            else:
                raise Exception('Illegal type \'{0}\' for diatonic pitch {1}'.format(type(tp[1]), tp[1]))
            tps.append((tp[0], diatonic_pitch.chromatic_distance))

        return tps




