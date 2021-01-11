"""

File: hc_expression.py

Purpose: Class that parses an hc_expression (text) and interprets against harmonic contexts.

"""
from harmonicmodel.chord_template import ChordTemplate
from harmonicmodel.tertian_chord_template import TertianChordTemplate, TertianChordType
from timemodel.duration import Duration
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.interval import Interval
import re
import logging

from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from harmoniccontext.harmonic_context import HarmonicContext


class HCExpression(object):
    """
    Class that defines the harmonic context expression language, implements it, and provides and interpreter
    that generates a harmonic context using a contextual set of HC's
    """

    GROUP_REFERENCE_0 = 'Reference0'
    GROUP_REFERENCE_0_TAG = '?P<' + GROUP_REFERENCE_0 + '>'
    GROUP_REFERENCE_0P = 'Reference0P'
    GROUP_REFERENCE_0P_TAG = '?P<' + GROUP_REFERENCE_0P + '>'

    N = '(0|[1-9]([0-9])*)'
    REFERENCE_PRIMATIVE = '@(' + GROUP_REFERENCE_0_TAG + N + ')'
    REFERENCE_PARENED = '\(' + '@(' + GROUP_REFERENCE_0P_TAG + N + ')' + '\)'
    REFERENCE = '(' + REFERENCE_PARENED + '|' + REFERENCE_PRIMATIVE + ')'

    INTERVAL_TEXT = '(P|m|M|A|d):' + N
    GROUP_INTERVAL_DISTANCE = 'IntervalDistance'
    GROUP_INTERVAL_DISTANCE_TAG = '?P<' + GROUP_INTERVAL_DISTANCE + '>'
    INTERVAL_DISTANCE = '(' + GROUP_INTERVAL_DISTANCE_TAG + INTERVAL_TEXT + ')'

    GROUP_SCALE_DISTANCE = 'ScaleDistance'
    GROUP_SCALE_DISTANCE_TAG = '?P<' + GROUP_SCALE_DISTANCE + '>'
    SCALE_DISTANCE = 'd(' + GROUP_SCALE_DISTANCE_TAG + N + ')'

    KEY_DISTANCE = '(' + INTERVAL_DISTANCE + ')?'
    # KEY_DISTANCE = '(' + INTERVAL_DISTANCE + '|' + SCALE_DISTANCE + ')?'

    KEY_LTR = '[A-Ga-g](bb|b|##|#)?'
    GROUP_KEY_LTR = 'KeyLtr'
    GROUP_KEY_LTR_TAG = '?P<' + GROUP_KEY_LTR + '>'

    REF_DIST = REFERENCE
    ABS_KEY = '(' + GROUP_KEY_LTR_TAG + KEY_LTR + ')'
    KEY = '(' + ABS_KEY + '|' + REF_DIST + ')' + KEY_DISTANCE

    MODALITIES = '(Major|NaturalMinor|MelodicMinor|HarmonicMinor|Natural|Melodic|Harmonic|Minor)'
    GROUP_MODALITY_NAME = 'ModalityName'
    GROUP_MODALITY_NAME_TAG = '?P<' + GROUP_MODALITY_NAME + '>'
    EXPLICIT_MODALITY = '(' + GROUP_MODALITY_NAME_TAG + MODALITIES + ')'

    GROUP_REFERENCE_1 = 'Reference1'
    GROUP_REFERENCE_1_TAG = '?P<' + GROUP_REFERENCE_1 + '>'
    MODALITY_REFERENCE_1 = '@(' + GROUP_REFERENCE_1_TAG + N + ')'

    GROUP_REFERENCE_1P = 'Reference1P'
    GROUP_REFERENCE_1P_TAG = '?P<' + GROUP_REFERENCE_1P + '>'
    MODALITY_REFERENCE_1_PARENED = '\(' + '@(' + GROUP_REFERENCE_1P_TAG + N + ')' + '\)'
    MODALITY_REFERENCE = '(' + MODALITY_REFERENCE_1_PARENED + '|' + MODALITY_REFERENCE_1 + ')'

    GROUP_MODAL_INDEX = 'ModalIndex'
    GROUP_MODAL_INDEX_TAG = '?P<' + GROUP_MODAL_INDEX + '>'
    GROUP_MODAL_REFERENCE = 'ModalReference'
    GROUP_MODAL_REFERENCE_TAG = '?P<' + GROUP_MODAL_REFERENCE + '>'
    MODAL_INDEX_CONTENT = '(' + GROUP_MODAL_INDEX_TAG + N + ')|(@(' + GROUP_MODAL_REFERENCE_TAG + N + '))'
    MODAL_INDEX = '\((' + MODAL_INDEX_CONTENT + ')\)'

    MODALITY = '(-(' + EXPLICIT_MODALITY + '|' + MODALITY_REFERENCE + ')(' + MODAL_INDEX + ')?)?'

    GROUP_CHORD_NAME = 'ChordName'
    GROUP_CHORD_NAME_TAG = '?P<' + GROUP_CHORD_NAME + '>'
    CHORD_NAME = GROUP_CHORD_NAME_TAG + TertianChordTemplate.CHORD_NAMES

    GROUP_EXPLICIT_CHORD_DEGREE = 'ExplicitChordDegree'
    GROUP_EXPLICIT_CHORD_DEGREE_TAG = '?P<' + GROUP_EXPLICIT_CHORD_DEGREE + '>'
    EXPLICIT_CHORD_DEGREE = GROUP_EXPLICIT_CHORD_DEGREE_TAG + TertianChordTemplate.SCALE_DEGREE

    GROUP_CHORD_DEGREE_REFERENCE = 'ChordDegreeReference'
    GROUP_CHORD_DEGREE_REFERENCE_TAG = '?P<' + GROUP_CHORD_DEGREE_REFERENCE + '>'
    CHORD_DEGREE_REFERENCE = '(@(' + GROUP_CHORD_DEGREE_REFERENCE_TAG + N + '))'
    GROUP_CHORD_DEGREE_REFERENCE_PAREND = 'ChordDegreeReferenceP'
    GROUP_CHORD_DEGREE_REFERENCE_PAREND_TAG = '?P<' + GROUP_CHORD_DEGREE_REFERENCE_PAREND + '>'
    CHORD_DEGREE_REFERENCE_P = '(\(@(' + GROUP_CHORD_DEGREE_REFERENCE_PAREND_TAG + N + ')\))'
    CHORD_DEGREE_REF = '(' + CHORD_DEGREE_REFERENCE_P + '|' + CHORD_DEGREE_REFERENCE + ')'

    CHORD_CONTENT = '((' + EXPLICIT_CHORD_DEGREE + '|' + CHORD_DEGREE_REF + ')(' + CHORD_NAME + ')?)'
    CHORD = '(:' + CHORD_CONTENT + ')?'

    HC_EXPRESSION_STRING = KEY + MODALITY + CHORD + '$'

    HC_EXPRESSION = re.compile(HC_EXPRESSION_STRING)

    def __init__(self, key, key_modality, chord_numeral, key_modifier, modality_index, chord_type):
        """
        Constructor
        :param key: Explicit key, e.g. A# as string, or hc reference as integer.
        :param key_modality: Explicit modality, e.g. Major as string, or hc reference as integer.
        :param chord_numeral: Explicit chord numeral, e.g. vii as string, or hc reference as integer.
        :param key_modifier: key modifier as interval or None.
        :param modality_index: Modality index as int string, e.g. '2' or hc reference as integer, or None.
        :param chord_type: Chord type as string, or hc reference as integer.
        """
        self.__key = key
        self.__key_modality = key_modality
        self.__chord_numeral = chord_numeral
        self.__key_modifier = key_modifier
        self.__modality_index = modality_index
        self.__chord_type = chord_type

    @staticmethod
    def create(text_expression):
        """
        Create an HCExpression from a textual rendering of hc expression.
        :param text_expression:
        :return:
        """
        key, key_modality, chord_numeral, key_modifier, modality_index, chord_name = HCExpression.parse(text_expression)
        return HCExpression(key, key_modality, chord_numeral, key_modifier, modality_index, chord_name)

    @property
    def key(self):
        return self.__key

    @property
    def key_modality(self):
        return self.__key_modality

    @property
    def chord_numeral(self):
        return self.__chord_numeral

    @property
    def key_modifier(self):
        return self.__key_modifier

    @property
    def modality_index(self):
        return self.__modality_index

    @property
    def chord_type(self):
        return self.__chord_type

    def interpret(self, hc_list, duration=Duration(1, 4)):
        """
        Give a list of HarmonicContext's, interpret the HCExpression into a HarmonicContext.
        :param hc_list:
        :param duration:
        :return: HarmonicContext
        """
        if isinstance(self.key, str):
            key_tone = DiatonicToneCache.get_tone(self.key)
        else:
            if self.key not in range(0, len(hc_list)):
                raise Exception('@{0} not in range.'.format(self.key))
            key_tone = hc_list[self.key].tonality.diatonic_tone

        if self.key_modifier is not None:
            key_tone = self.key_modifier.get_end_tone(key_tone)

        if self.modality_index:
            if isinstance(self.modality_index, str):
                modal_index = int(self.modality_index)
            else:
                if self.modality_index not in range(0, len(hc_list)):
                    raise Exception('@{0} not in range.'.format(self.modality_index))
                modal_index = hc_list[self.modality_index].tonality.modal_index
        else:
            modal_index = 0

        if isinstance(self.key_modality, str):
            modality_type = ModalityType(self.key_modality)
        else:
            if self.key_modality not in range(0, len(hc_list)):
                raise Exception('@{0} not in range.'.format(self.key_modality))
            modality_type = hc_list[self.key_modality].tonality.modality_type

        #  Note: chord_numeral is origin 1
        if isinstance(self.chord_numeral, str):
            chord_numeral = ChordTemplate.SCALE_DEGREE_MAP[self.chord_numeral]
        else:
            if self.chord_numeral not in range(0, len(hc_list)):
                raise Exception('@{0} not in range.'.format(self.chord_numeral))
            chord_numeral = hc_list[self.chord_numeral].chord.chord_template.scale_degree

        if self.chord_type:
            if isinstance(self.chord_type, str):
                chord_type = TertianChordType.to_type(self.chord_type)
            else:
                if self.chord_type not in range(0, len(hc_list)):
                    raise Exception('@{0} not in range.'.format(self.chord_type))
                chord_type = hc_list[self.chord_type].chord.chord_type
        else:
            chord_type = None

        tonality = Tonality.create(modality_type, key_tone, modal_index)
        chord_template = ChordTemplate.generic_chord_template_parse(
            ChordTemplate.SCALE_DEGREE_REVERSE_MAP[chord_numeral] + (str(chord_type) if chord_type else ''))
        chord = chord_template.create_chord(tonality)

        hc = HarmonicContext(tonality, chord, duration)

        return hc

    def __str__(self):
        key = '@' + str(self.key) if isinstance(self.key, int) else self.key
        chord_numeral = '@' + str(self.chord_numeral) if isinstance(self.chord_numeral, int) else self.chord_numeral
        key_modality = '@' + str(self.key_modality) if isinstance(self.key_modality, int) else self.key_modality
        chord_name = '(@' + str(self.chord_type) + ')' if self.chord_type and isinstance(self.chord_type, int) else \
            self.chord_type
        key_modifier = '(d' + str(self.key_modifier) + ')' if self.key_modifier and isinstance(self.key_modifier, int) \
            else self.key_modifier
        s = '{0}{1}-{2}{3}/{4}{5}'.format(key,
                                          key_modifier if key_modifier else '',
                                          key_modality,
                                          self.modality_index if self.modality_index else '',
                                          chord_numeral,
                                          chord_name if chord_name else '')
        return s

    @staticmethod
    def parse(expression_text):
        """
        Parse an input string into a parts of HCExpression

        Args:
          expression_text: string input representing hc expression
        Returns:
          HC Expression parts.
        """
        if not expression_text:
            raise Exception('Unable to parse hc expression string to completion: {0}'.format(expression_text))
        m = HCExpression.HC_EXPRESSION.match(expression_text)
        if not m:
            raise Exception('Unable to parse hc expression string to completion: {0}'.format(expression_text))

        ref_0 = m.group(HCExpression.GROUP_REFERENCE_0)
        ref_0_p = m.group(HCExpression.GROUP_REFERENCE_0P)
        key_ltr = m.group(HCExpression.GROUP_KEY_LTR)
        # scale_distance = m.group(HCExpression.GROUP_SCALE_DISTANCE)
        interval_distance = m.group(HCExpression.GROUP_INTERVAL_DISTANCE)
        if interval_distance:
            try:
                interval_distance = Interval.parse(interval_distance)
            except Exception as e:
                print('Exception parsing interval {0} - {1}'.format(interval_distance, e))
                return
        modality_name = m.group(HCExpression.GROUP_MODALITY_NAME)
        ref_1 = m.group(HCExpression.GROUP_REFERENCE_1)
        ref_1_p = m.group(HCExpression.GROUP_REFERENCE_1P)
        modal_index = m.group(HCExpression.GROUP_MODAL_INDEX)
        modal_index_ref = m.group(HCExpression.GROUP_MODAL_REFERENCE)
        explicit_chord_degree = m.group(HCExpression.GROUP_EXPLICIT_CHORD_DEGREE)
        chord_degree_reff = m.group(HCExpression.GROUP_CHORD_DEGREE_REFERENCE)
        chord_degree_reff_p = m.group(HCExpression.GROUP_CHORD_DEGREE_REFERENCE_PAREND)
        chord_explicit_name = m.group(HCExpression.GROUP_CHORD_NAME)

        key = int(ref_0) if ref_0 else int(ref_0_p) if ref_0_p else key_ltr
        key_modality = int(ref_1) if ref_1 else int(ref_1_p) if ref_1_p else modality_name if modality_name else None
        if key_modality == 'Minor':
            key_modality = 'MelodicMinor'
        if key_modality == 'Natural':
            key_modality = 'NaturalMinor'
        if key_modality == 'Melodic':
            key_modality = 'MelodicMinor'
        if key_modality == 'Harmonic':
            key_modality = 'HarmonicMinor'
        chord_numeral = int(chord_degree_reff) if chord_degree_reff else int(chord_degree_reff_p) \
            if chord_degree_reff_p else explicit_chord_degree if explicit_chord_degree else None

        key_modifier = interval_distance if interval_distance else None
        # key_modifier = interval_distance if interval_distance else int(scale_distance) if scale_distance else None
        modality_index = int(modal_index_ref) if modal_index_ref else str(modal_index) if modal_index else None
        chord_type = chord_explicit_name if chord_explicit_name else None

        # interited qualities
        if isinstance(key, int):
            key_modality = key if key_modality is None else key_modality
            # chord type inherits from chord_numeral if not none, else from key.
            if chord_type is None:
                if chord_numeral is not None:
                    chord_type = chord_numeral if isinstance(chord_numeral, int) else None
                else:
                    chord_type = key
            chord_numeral = key if chord_numeral is None else chord_numeral

        if chord_numeral is None:
            chord_numeral = 'i'
        if key_modality is None:
            key_modality = 'Major'

        logging.info('{0}, {1}, {2}, {3}'.format(key, key_modality, chord_numeral,
                                                 key_modifier, modality_index, chord_type))

        return key, key_modality, chord_numeral, key_modifier, modality_index, chord_type
