"""
File: line_grammar_executor.py

Purpose: Convenience class allowing execution of parsing line grammar strings into line and harmonic context track.
"""

import antlr4

from structure.LineGrammar.LineGrammarParser import LineGrammarParser
from structure.LineGrammar.LineGrammarLexer import LineGrammarLexer


class LineGrammarExecutor(object):
    """
    Class to parse a string into a line and an hct.
    """

    def __init__(self):
        pass

    def parse(self, line_text):
        """
        Parse command
        :param line_text:
        :return: (line, hct)
        """
        lexer = LineGrammarLexer(antlr4.InputStream(line_text))
        stream = antlr4.CommonTokenStream(lexer)
        parser = LineGrammarParser(stream)

        if parser.motif() is None:
            raise Exception('Parsing error.')

        return parser.lc.line, parser.lc.hct
