"""

File: substitution_pattern.py

Purpose: A 'setup' class that takes the burden of 'find' and 'replacement' pattern, along with conversion HCExpression
         which is used in other contexts for find/replace type of operations. (ref. TPatSub)

"""
from search.melodicsearch.melodic_search_analysis import MelodicSearchAnalysis
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from transformation.patsub.hc_expression import HCExpression


class SubstitutionPattern(object):

    def __init__(self, source_pattern_line, source_pattern_hct,
                 target_pattern_line, target_pattern_hct, target_hc_exprs, target_melodic_form=None):
        """
        Constructor.
        :param source_pattern_line: Line representing a 'find' pattern - usually the pattern used for search.
        :param source_pattern_hct:  HCT representing a 'find' pattern - accompanying pattern for the find.
        :param target_pattern_line: The replacement pattern - represents what would be used to replace a found instance.
        :param target_pattern_hct: HCT for the replacement pattern.
        :param target_hc_exprs: HCExpression used to build replacement instance hct based on find instance hct.
        :param target_melodic_form: Form for target pattern, holding other constraints.
        """
        self.__source_pattern_line = source_pattern_line
        self.__source_pattern_hct = source_pattern_hct
        self.__target_pattern_line = target_pattern_line
        self.__target_pattern_hct = target_pattern_hct
        self.__target_hc_exprs = [HCExpression.create(h) if isinstance(h, str) else h for h in target_hc_exprs]
        self.__target_melodic_form = target_melodic_form

        self._validate_source_target_hc_exprs()

        self.__target_analysis = MelodicSearchAnalysis(target_pattern_line, target_pattern_hct)
        min_pitch, max_pitch = self.compute_min_max_pitches(self.target_pattern_line.get_all_notes())
        self.__target_height = max_pitch.chromatic_distance - min_pitch.chromatic_distance

    @staticmethod
    def create(source_pattern_expr, target_pattern_expr, target_hc_exprs):
        """
        Constructor.
        :param source_pattern_expr: 'find' pattern expression - for line and hct.
        :param target_pattern_expr: 'replacement' pattern expression - for replacement line and hct.
        :param target_hc_exprs: HCExpression to build target instance from 'find' instances.
        :return:
        """
        lge = LineGrammarExecutor()
        source_line, source_hct = lge.parse(source_pattern_expr)
        target_line, target_hct = lge.parse(target_pattern_expr)

        return SubstitutionPattern(source_line, source_hct, target_line, target_hct, target_hc_exprs)

    @property
    def source_pattern_line(self):
        return self.__source_pattern_line

    @property
    def source_pattern_hct(self):
        return self.__source_pattern_hct

    @property
    def target_pattern_line(self):
        return self.__target_pattern_line

    @property
    def target_pattern_hct(self):
        return self.__target_pattern_hct

    @property
    def target_hc_exprs(self):
        return self.__target_hc_exprs

    @property
    def target_melodic_form(self):
        return self.__target_melodic_form

    @property
    def target_analysis(self):
        return self.__target_analysis

    @property
    def target_height(self):
        return self.__target_height

    def _validate_source_target_hc_exprs(self):
        if len(self.target_hc_exprs) != len(self.target_pattern_hct):
            raise Exception('Number of hc expression not equal to number of hc\'s in target pattern.')

        # This check has philosophical arguments. Should target pattern hct compute identical to the expressions
        # based on the source pattern.
        # It is possible to say that the analysis based on the target hcs was only to id the chordal tones but
        # not necessarily to what the exprs produce.
        for hc, hc_expr in zip(self.target_pattern_hct.hc_list(), self.target_hc_exprs):
            if not hc.is_equal(hc_expr.interpret(self.source_pattern_hct, hc.duration)):
                raise Exception('HCExpression {0} does not produce HC {1}, but {2} instead.'.
                                format(hc_expr, hc, hc_expr.interpret(self.source_pattern_hct, hc.duration)))

    @staticmethod
    def compute_min_max_pitches(notes):
        min_pitch = None
        max_pitch = None
        for n in notes:
            p = n.diatonic_pitch
            min_pitch = p if min_pitch is None else p if p.chromatic_distance < min_pitch.chromatic_distance else \
                min_pitch
            max_pitch = p if max_pitch is None else p if p.chromatic_distance > max_pitch.chromatic_distance else \
                max_pitch

        return min_pitch, max_pitch
