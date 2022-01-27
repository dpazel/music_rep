# Generated from /Users/dpazel/PycharmProjects/music_rep_melody/resources/LineGrammar.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LineGrammarParser import LineGrammarParser
else:
    from LineGrammarParser import LineGrammarParser

from structure.LineGrammar.core.line_constructor import LineConstructor
import sys


# This class defines a complete listener for a parse tree produced by LineGrammarParser.
class LineGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by LineGrammarParser#motif.
    def enterMotif(self, ctx:LineGrammarParser.MotifContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#motif.
    def exitMotif(self, ctx:LineGrammarParser.MotifContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#motificElement.
    def enterMotificElement(self, ctx:LineGrammarParser.MotificElementContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#motificElement.
    def exitMotificElement(self, ctx:LineGrammarParser.MotificElementContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#primitiveNote.
    def enterPrimitiveNote(self, ctx:LineGrammarParser.PrimitiveNoteContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#primitiveNote.
    def exitPrimitiveNote(self, ctx:LineGrammarParser.PrimitiveNoteContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#beam.
    def enterBeam(self, ctx:LineGrammarParser.BeamContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#beam.
    def exitBeam(self, ctx:LineGrammarParser.BeamContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#tuplet.
    def enterTuplet(self, ctx:LineGrammarParser.TupletContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#tuplet.
    def exitTuplet(self, ctx:LineGrammarParser.TupletContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#pitch.
    def enterPitch(self, ctx:LineGrammarParser.PitchContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#pitch.
    def exitPitch(self, ctx:LineGrammarParser.PitchContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#tone.
    def enterTone(self, ctx:LineGrammarParser.ToneContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#tone.
    def exitTone(self, ctx:LineGrammarParser.ToneContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#duration.
    def enterDuration(self, ctx:LineGrammarParser.DurationContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#duration.
    def exitDuration(self, ctx:LineGrammarParser.DurationContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#durationFraction.
    def enterDurationFraction(self, ctx:LineGrammarParser.DurationFractionContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#durationFraction.
    def exitDurationFraction(self, ctx:LineGrammarParser.DurationFractionContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#tonality.
    def enterTonality(self, ctx:LineGrammarParser.TonalityContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#tonality.
    def exitTonality(self, ctx:LineGrammarParser.TonalityContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#chordTemplate.
    def enterChordTemplate(self, ctx:LineGrammarParser.ChordTemplateContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#chordTemplate.
    def exitChordTemplate(self, ctx:LineGrammarParser.ChordTemplateContext):
        pass


    # Enter a parse tree produced by LineGrammarParser#harmonicTag.
    def enterHarmonicTag(self, ctx:LineGrammarParser.HarmonicTagContext):
        pass

    # Exit a parse tree produced by LineGrammarParser#harmonicTag.
    def exitHarmonicTag(self, ctx:LineGrammarParser.HarmonicTagContext):
        pass



del LineGrammarParser