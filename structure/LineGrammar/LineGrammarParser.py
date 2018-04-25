# Generated from /Users/dpazel/PycharmProjects/music_rep_melody/resources/LineGrammar.g4 by ANTLR 4.7
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from structure.LineGrammar.core.line_constructor import LineConstructor
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\30")
        buf.write("\u009b\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2")
        buf.write("\3\2\6\2\35\n\2\r\2\16\2\36\3\2\3\2\3\3\3\3\3\3\3\3\5")
        buf.write("\3\'\n\3\3\3\3\3\5\3+\n\3\3\4\3\4\3\4\3\4\7\4\61\n\4\f")
        buf.write("\4\16\4\64\13\4\5\4\66\n\4\3\4\3\4\3\4\5\4;\n\4\3\4\3")
        buf.write("\4\3\5\3\5\3\5\6\5B\n\5\r\5\16\5C\3\5\3\5\3\5\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\6\6Q\n\6\r\6\16\6R\3\6\3\6\3")
        buf.write("\6\3\7\3\7\3\7\3\7\3\7\5\7]\n\7\3\7\3\7\3\b\3\b\3\b\3")
        buf.write("\b\5\be\n\b\3\b\3\b\5\bi\n\b\3\b\3\b\3\t\3\t\3\t\3\t\3")
        buf.write("\t\3\t\3\t\3\t\3\t\5\tv\n\t\3\n\3\n\3\n\3\n\3\n\3\13\3")
        buf.write("\13\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f")
        buf.write("\5\f\u008b\n\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r")
        buf.write("\5\r\u0097\n\r\3\r\3\r\3\r\2\2\16\2\4\6\b\n\f\16\20\22")
        buf.write("\24\26\30\2\2\2\u00a0\2\32\3\2\2\2\4*\3\2\2\2\6\65\3\2")
        buf.write("\2\2\b>\3\2\2\2\nH\3\2\2\2\fW\3\2\2\2\16d\3\2\2\2\20u")
        buf.write("\3\2\2\2\22w\3\2\2\2\24|\3\2\2\2\26\u008a\3\2\2\2\30\u008c")
        buf.write("\3\2\2\2\32\34\7\16\2\2\33\35\5\4\3\2\34\33\3\2\2\2\35")
        buf.write("\36\3\2\2\2\36\34\3\2\2\2\36\37\3\2\2\2\37 \3\2\2\2 !")
        buf.write("\7\17\2\2!\3\3\2\2\2\"#\5\6\4\2#$\b\3\1\2$\'\3\2\2\2%")
        buf.write("\'\5\30\r\2&\"\3\2\2\2&%\3\2\2\2\'+\3\2\2\2(+\5\b\5\2")
        buf.write(")+\5\n\6\2*&\3\2\2\2*(\3\2\2\2*)\3\2\2\2+\5\3\2\2\2,-")
        buf.write("\5\20\t\2-\62\b\4\1\2./\7\13\2\2/\61\b\4\1\2\60.\3\2\2")
        buf.write("\2\61\64\3\2\2\2\62\60\3\2\2\2\62\63\3\2\2\2\63\66\3\2")
        buf.write("\2\2\64\62\3\2\2\2\65,\3\2\2\2\65\66\3\2\2\2\66\67\3\2")
        buf.write("\2\2\67:\5\f\7\289\7\f\2\29;\b\4\1\2:8\3\2\2\2:;\3\2\2")
        buf.write("\2;<\3\2\2\2<=\b\4\1\2=\7\3\2\2\2>?\7\3\2\2?A\b\5\1\2")
        buf.write("@B\5\4\3\2A@\3\2\2\2BC\3\2\2\2CA\3\2\2\2CD\3\2\2\2DE\3")
        buf.write("\2\2\2EF\7\4\2\2FG\b\5\1\2G\t\3\2\2\2HI\7\5\2\2IJ\5\20")
        buf.write("\t\2JK\7\6\2\2KL\7\r\2\2LM\7\7\2\2MN\7\3\2\2NP\b\6\1\2")
        buf.write("OQ\5\4\3\2PO\3\2\2\2QR\3\2\2\2RP\3\2\2\2RS\3\2\2\2ST\3")
        buf.write("\2\2\2TU\7\4\2\2UV\b\6\1\2V\13\3\2\2\2WX\5\16\b\2X\\\b")
        buf.write("\7\1\2YZ\7\b\2\2Z[\7\r\2\2[]\b\7\1\2\\Y\3\2\2\2\\]\3\2")
        buf.write("\2\2]^\3\2\2\2^_\b\7\1\2_\r\3\2\2\2`a\7\24\2\2ae\b\b\1")
        buf.write("\2bc\7\21\2\2ce\b\b\1\2d`\3\2\2\2db\3\2\2\2eh\3\2\2\2")
        buf.write("fi\7\25\2\2gi\7\21\2\2hf\3\2\2\2hg\3\2\2\2hi\3\2\2\2i")
        buf.write("j\3\2\2\2jk\b\b\1\2k\17\3\2\2\2lm\7\23\2\2mv\b\t\1\2n")
        buf.write("o\7\22\2\2ov\b\t\1\2pq\7\5\2\2qr\5\22\n\2rs\7\7\2\2st")
        buf.write("\b\t\1\2tv\3\2\2\2ul\3\2\2\2un\3\2\2\2up\3\2\2\2v\21\3")
        buf.write("\2\2\2wx\7\r\2\2xy\7\b\2\2yz\7\r\2\2z{\b\n\1\2{\23\3\2")
        buf.write("\2\2|}\5\16\b\2}~\7\f\2\2~\177\7\26\2\2\177\u0080\b\13")
        buf.write("\1\2\u0080\25\3\2\2\2\u0081\u0082\5\16\b\2\u0082\u0083")
        buf.write("\7\f\2\2\u0083\u0084\7\30\2\2\u0084\u0085\b\f\1\2\u0085")
        buf.write("\u008b\3\2\2\2\u0086\u0087\7\27\2\2\u0087\u008b\b\f\1")
        buf.write("\2\u0088\u0089\7\22\2\2\u0089\u008b\b\f\1\2\u008a\u0081")
        buf.write("\3\2\2\2\u008a\u0086\3\2\2\2\u008a\u0088\3\2\2\2\u008b")
        buf.write("\27\3\2\2\2\u008c\u0096\7\t\2\2\u008d\u008e\5\24\13\2")
        buf.write("\u008e\u008f\7\b\2\2\u008f\u0090\5\26\f\2\u0090\u0091")
        buf.write("\b\r\1\2\u0091\u0097\3\2\2\2\u0092\u0093\7\b\2\2\u0093")
        buf.write("\u0094\5\26\f\2\u0094\u0095\b\r\1\2\u0095\u0097\3\2\2")
        buf.write("\2\u0096\u008d\3\2\2\2\u0096\u0092\3\2\2\2\u0097\u0098")
        buf.write("\3\2\2\2\u0098\u0099\7\n\2\2\u0099\31\3\2\2\2\20\36&*")
        buf.write("\62\65:CR\\dhu\u008a\u0096")
        return buf.getvalue()


class LineGrammarParser ( Parser ):

    grammarFileName = "LineGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "']'", "'('", "','", "')'", "':'", 
                     "'<'", "'>'", "'@'", "'-'", "<INVALID>", "'{'", "'}'", 
                     "<INVALID>", "'b'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "DOT", "TIE", "INT", "LINEBEGIN", "LINEEND", 
                      "WS", "COMMON_TONE_ALTERATION_LETTER", "COMMON_DURATION_CHORD_NUMERAL_LETTERS", 
                      "DURATIONLETTER", "TONELETTER", "ALTERATION", "MODALITY", 
                      "CHORDNUMERAL", "CHORDMODALITY" ]

    RULE_motif = 0
    RULE_motificElement = 1
    RULE_primitiveNote = 2
    RULE_beam = 3
    RULE_tuplet = 4
    RULE_pitch = 5
    RULE_tone = 6
    RULE_duration = 7
    RULE_durationFraction = 8
    RULE_tonality = 9
    RULE_chordTemplate = 10
    RULE_harmonicTag = 11

    ruleNames =  [ "motif", "motificElement", "primitiveNote", "beam", "tuplet", 
                   "pitch", "tone", "duration", "durationFraction", "tonality", 
                   "chordTemplate", "harmonicTag" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    DOT=9
    TIE=10
    INT=11
    LINEBEGIN=12
    LINEEND=13
    WS=14
    COMMON_TONE_ALTERATION_LETTER=15
    COMMON_DURATION_CHORD_NUMERAL_LETTERS=16
    DURATIONLETTER=17
    TONELETTER=18
    ALTERATION=19
    MODALITY=20
    CHORDNUMERAL=21
    CHORDMODALITY=22

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



        self.lc = LineConstructor();
        self._notelist = list()


    class MotifContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LINEBEGIN(self):
            return self.getToken(LineGrammarParser.LINEBEGIN, 0)

        def LINEEND(self):
            return self.getToken(LineGrammarParser.LINEEND, 0)

        def motificElement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LineGrammarParser.MotificElementContext)
            else:
                return self.getTypedRuleContext(LineGrammarParser.MotificElementContext,i)


        def getRuleIndex(self):
            return LineGrammarParser.RULE_motif

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMotif" ):
                listener.enterMotif(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMotif" ):
                listener.exitMotif(self)




    def motif(self):

        localctx = LineGrammarParser.MotifContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_motif)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(LineGrammarParser.LINEBEGIN)
            self.state = 26 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 25
                self.motificElement()
                self.state = 28 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << LineGrammarParser.T__0) | (1 << LineGrammarParser.T__2) | (1 << LineGrammarParser.T__6) | (1 << LineGrammarParser.COMMON_TONE_ALTERATION_LETTER) | (1 << LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS) | (1 << LineGrammarParser.DURATIONLETTER) | (1 << LineGrammarParser.TONELETTER))) != 0)):
                    break

            self.state = 30
            self.match(LineGrammarParser.LINEEND)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MotificElementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._primitiveNote = None # PrimitiveNoteContext

        def beam(self):
            return self.getTypedRuleContext(LineGrammarParser.BeamContext,0)


        def tuplet(self):
            return self.getTypedRuleContext(LineGrammarParser.TupletContext,0)


        def primitiveNote(self):
            return self.getTypedRuleContext(LineGrammarParser.PrimitiveNoteContext,0)


        def harmonicTag(self):
            return self.getTypedRuleContext(LineGrammarParser.HarmonicTagContext,0)


        def getRuleIndex(self):
            return LineGrammarParser.RULE_motificElement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMotificElement" ):
                listener.enterMotificElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMotificElement" ):
                listener.exitMotificElement(self)




    def motificElement(self):

        localctx = LineGrammarParser.MotificElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_motificElement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 36
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [LineGrammarParser.T__2, LineGrammarParser.COMMON_TONE_ALTERATION_LETTER, LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS, LineGrammarParser.DURATIONLETTER, LineGrammarParser.TONELETTER]:
                    self.state = 32
                    localctx._primitiveNote = self.primitiveNote()
                    self.lc.add_note(localctx._primitiveNote.n)
                    pass
                elif token in [LineGrammarParser.T__6]:
                    self.state = 35
                    self.harmonicTag()
                    pass
                else:
                    raise NoViableAltException(self)

                pass

            elif la_ == 2:
                self.state = 38
                self.beam()
                pass

            elif la_ == 3:
                self.state = 39
                self.tuplet()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PrimitiveNoteContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.n = None
            self.dots = 0
            self.dur = None
            self.ties = False
            self._duration = None # DurationContext
            self._pitch = None # PitchContext

        def pitch(self):
            return self.getTypedRuleContext(LineGrammarParser.PitchContext,0)


        def duration(self):
            return self.getTypedRuleContext(LineGrammarParser.DurationContext,0)


        def TIE(self):
            return self.getToken(LineGrammarParser.TIE, 0)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(LineGrammarParser.DOT)
            else:
                return self.getToken(LineGrammarParser.DOT, i)

        def getRuleIndex(self):
            return LineGrammarParser.RULE_primitiveNote

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitiveNote" ):
                listener.enterPrimitiveNote(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitiveNote" ):
                listener.exitPrimitiveNote(self)




    def primitiveNote(self):

        localctx = LineGrammarParser.PrimitiveNoteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_primitiveNote)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << LineGrammarParser.T__2) | (1 << LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS) | (1 << LineGrammarParser.DURATIONLETTER))) != 0):
                self.state = 42
                localctx._duration = self.duration()
                localctx.dur = localctx._duration.d
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==LineGrammarParser.DOT:
                    self.state = 44
                    self.match(LineGrammarParser.DOT)
                    localctx.dots = localctx.dots + 1
                    self.state = 50
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 53
            localctx._pitch = self.pitch()
            self.state = 56
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==LineGrammarParser.TIE:
                self.state = 54
                self.match(LineGrammarParser.TIE)
                localctx.ties = True


            localctx.n = self.lc.construct_note(localctx._pitch.p, localctx.dur, localctx.dots, localctx.ties)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BeamContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def motificElement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LineGrammarParser.MotificElementContext)
            else:
                return self.getTypedRuleContext(LineGrammarParser.MotificElementContext,i)


        def getRuleIndex(self):
            return LineGrammarParser.RULE_beam

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBeam" ):
                listener.enterBeam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBeam" ):
                listener.exitBeam(self)




    def beam(self):

        localctx = LineGrammarParser.BeamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_beam)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(LineGrammarParser.T__0)
            self.lc.start_level()
            self.state = 63 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 62
                self.motificElement()
                self.state = 65 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << LineGrammarParser.T__0) | (1 << LineGrammarParser.T__2) | (1 << LineGrammarParser.T__6) | (1 << LineGrammarParser.COMMON_TONE_ALTERATION_LETTER) | (1 << LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS) | (1 << LineGrammarParser.DURATIONLETTER) | (1 << LineGrammarParser.TONELETTER))) != 0)):
                    break

            self.state = 67
            self.match(LineGrammarParser.T__1)
            self.lc.end_level()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TupletContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._duration = None # DurationContext
            self.dur_int = None # Token

        def duration(self):
            return self.getTypedRuleContext(LineGrammarParser.DurationContext,0)


        def INT(self):
            return self.getToken(LineGrammarParser.INT, 0)

        def motificElement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LineGrammarParser.MotificElementContext)
            else:
                return self.getTypedRuleContext(LineGrammarParser.MotificElementContext,i)


        def getRuleIndex(self):
            return LineGrammarParser.RULE_tuplet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTuplet" ):
                listener.enterTuplet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTuplet" ):
                listener.exitTuplet(self)




    def tuplet(self):

        localctx = LineGrammarParser.TupletContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_tuplet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.match(LineGrammarParser.T__2)
            self.state = 71
            localctx._duration = self.duration()
            self.state = 72
            self.match(LineGrammarParser.T__3)
            self.state = 73
            localctx.dur_int = self.match(LineGrammarParser.INT)
            self.state = 74
            self.match(LineGrammarParser.T__4)
            self.state = 75
            self.match(LineGrammarParser.T__0)
            self.lc.start_level(localctx._duration.d, dur_int=(0 if localctx.dur_int is None else int(localctx.dur_int.text)))
            self.state = 78 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 77
                self.motificElement()
                self.state = 80 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << LineGrammarParser.T__0) | (1 << LineGrammarParser.T__2) | (1 << LineGrammarParser.T__6) | (1 << LineGrammarParser.COMMON_TONE_ALTERATION_LETTER) | (1 << LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS) | (1 << LineGrammarParser.DURATIONLETTER) | (1 << LineGrammarParser.TONELETTER))) != 0)):
                    break

            self.state = 82
            self.match(LineGrammarParser.T__1)
            self.lc.end_level()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PitchContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.p = None
            self.tt = None
            self.alert = None
            self.reg = None
            self._tone = None # ToneContext
            self._INT = None # Token

        def tone(self):
            return self.getTypedRuleContext(LineGrammarParser.ToneContext,0)


        def INT(self):
            return self.getToken(LineGrammarParser.INT, 0)

        def getRuleIndex(self):
            return LineGrammarParser.RULE_pitch

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPitch" ):
                listener.enterPitch(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPitch" ):
                listener.exitPitch(self)




    def pitch(self):

        localctx = LineGrammarParser.PitchContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_pitch)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            localctx._tone = self.tone()
            localctx.tt = localctx._tone.t
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==LineGrammarParser.T__5:
                self.state = 87
                self.match(LineGrammarParser.T__5)
                self.state = 88
                localctx._INT = self.match(LineGrammarParser.INT)
                localctx.reg = (0 if localctx._INT is None else int(localctx._INT.text))


            localctx.p=self.lc.construct_pitch(localctx.tt, localctx.reg)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ToneContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.t = None
            self.ltr = None
            self._TONELETTER = None # Token
            self._COMMON_TONE_ALTERATION_LETTER = None # Token
            self.alter = None # Token

        def TONELETTER(self):
            return self.getToken(LineGrammarParser.TONELETTER, 0)

        def COMMON_TONE_ALTERATION_LETTER(self, i:int=None):
            if i is None:
                return self.getTokens(LineGrammarParser.COMMON_TONE_ALTERATION_LETTER)
            else:
                return self.getToken(LineGrammarParser.COMMON_TONE_ALTERATION_LETTER, i)

        def ALTERATION(self):
            return self.getToken(LineGrammarParser.ALTERATION, 0)

        def getRuleIndex(self):
            return LineGrammarParser.RULE_tone

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTone" ):
                listener.enterTone(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTone" ):
                listener.exitTone(self)




    def tone(self):

        localctx = LineGrammarParser.ToneContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_tone)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [LineGrammarParser.TONELETTER]:
                self.state = 94
                localctx._TONELETTER = self.match(LineGrammarParser.TONELETTER)
                localctx.ltr = (None if localctx._TONELETTER is None else localctx._TONELETTER.text)
                pass
            elif token in [LineGrammarParser.COMMON_TONE_ALTERATION_LETTER]:
                self.state = 96
                localctx._COMMON_TONE_ALTERATION_LETTER = self.match(LineGrammarParser.COMMON_TONE_ALTERATION_LETTER)
                localctx.ltr = (None if localctx._COMMON_TONE_ALTERATION_LETTER is None else localctx._COMMON_TONE_ALTERATION_LETTER.text)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 102
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 100
                localctx.alter = self.match(LineGrammarParser.ALTERATION)

            elif la_ == 2:
                self.state = 101
                localctx.alter = self.match(LineGrammarParser.COMMON_TONE_ALTERATION_LETTER)


            localctx.t=LineConstructor.construct_tone(localctx.ltr, (None if localctx.alter is None else localctx.alter.text) if localctx.alter is not None else None)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DurationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.d = None
            self._DURATIONLETTER = None # Token
            self._COMMON_DURATION_CHORD_NUMERAL_LETTERS = None # Token
            self._durationFraction = None # DurationFractionContext

        def DURATIONLETTER(self):
            return self.getToken(LineGrammarParser.DURATIONLETTER, 0)

        def COMMON_DURATION_CHORD_NUMERAL_LETTERS(self):
            return self.getToken(LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS, 0)

        def durationFraction(self):
            return self.getTypedRuleContext(LineGrammarParser.DurationFractionContext,0)


        def getRuleIndex(self):
            return LineGrammarParser.RULE_duration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDuration" ):
                listener.enterDuration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDuration" ):
                listener.exitDuration(self)




    def duration(self):

        localctx = LineGrammarParser.DurationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_duration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [LineGrammarParser.DURATIONLETTER]:
                self.state = 106
                localctx._DURATIONLETTER = self.match(LineGrammarParser.DURATIONLETTER)
                localctx.d = LineConstructor.construct_duration_by_shorthand((None if localctx._DURATIONLETTER is None else localctx._DURATIONLETTER.text)) 
                pass
            elif token in [LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS]:
                self.state = 108
                localctx._COMMON_DURATION_CHORD_NUMERAL_LETTERS = self.match(LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS)
                localctx.d = LineConstructor.construct_duration_by_shorthand((None if localctx._COMMON_DURATION_CHORD_NUMERAL_LETTERS is None else localctx._COMMON_DURATION_CHORD_NUMERAL_LETTERS.text)) 
                pass
            elif token in [LineGrammarParser.T__2]:
                self.state = 110
                self.match(LineGrammarParser.T__2)
                self.state = 111
                localctx._durationFraction = self.durationFraction()
                self.state = 112
                self.match(LineGrammarParser.T__4)
                localctx.d = LineConstructor.construct_duration(localctx._durationFraction.f[0], localctx._durationFraction.f[1])
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DurationFractionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.f = None
            self.numerator = None # Token
            self.denominator = None # Token

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(LineGrammarParser.INT)
            else:
                return self.getToken(LineGrammarParser.INT, i)

        def getRuleIndex(self):
            return LineGrammarParser.RULE_durationFraction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDurationFraction" ):
                listener.enterDurationFraction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDurationFraction" ):
                listener.exitDurationFraction(self)




    def durationFraction(self):

        localctx = LineGrammarParser.DurationFractionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_durationFraction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            localctx.numerator = self.match(LineGrammarParser.INT)
            self.state = 118
            self.match(LineGrammarParser.T__5)
            self.state = 119
            localctx.denominator = self.match(LineGrammarParser.INT)
            localctx.f = ((0 if localctx.numerator is None else int(localctx.numerator.text)), (0 if localctx.denominator is None else int(localctx.denominator.text)))
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TonalityContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.tonal = None
            self._tone = None # ToneContext
            self._MODALITY = None # Token

        def tone(self):
            return self.getTypedRuleContext(LineGrammarParser.ToneContext,0)


        def MODALITY(self):
            return self.getToken(LineGrammarParser.MODALITY, 0)

        def getRuleIndex(self):
            return LineGrammarParser.RULE_tonality

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTonality" ):
                listener.enterTonality(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTonality" ):
                listener.exitTonality(self)




    def tonality(self):

        localctx = LineGrammarParser.TonalityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_tonality)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 122
            localctx._tone = self.tone()
            self.state = 123
            self.match(LineGrammarParser.TIE)
            self.state = 124
            localctx._MODALITY = self.match(LineGrammarParser.MODALITY)
            localctx.tonal = self.lc.construct_tonality(localctx._tone.t, (None if localctx._MODALITY is None else localctx._MODALITY.text))
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ChordTemplateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.ctemplate = None
            self._tone = None # ToneContext
            self._CHORDMODALITY = None # Token
            self._CHORDNUMERAL = None # Token
            self._COMMON_DURATION_CHORD_NUMERAL_LETTERS = None # Token

        def tone(self):
            return self.getTypedRuleContext(LineGrammarParser.ToneContext,0)


        def CHORDMODALITY(self):
            return self.getToken(LineGrammarParser.CHORDMODALITY, 0)

        def CHORDNUMERAL(self):
            return self.getToken(LineGrammarParser.CHORDNUMERAL, 0)

        def COMMON_DURATION_CHORD_NUMERAL_LETTERS(self):
            return self.getToken(LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS, 0)

        def getRuleIndex(self):
            return LineGrammarParser.RULE_chordTemplate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChordTemplate" ):
                listener.enterChordTemplate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChordTemplate" ):
                listener.exitChordTemplate(self)




    def chordTemplate(self):

        localctx = LineGrammarParser.ChordTemplateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_chordTemplate)
        try:
            self.state = 136
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [LineGrammarParser.COMMON_TONE_ALTERATION_LETTER, LineGrammarParser.TONELETTER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 127
                localctx._tone = self.tone()
                self.state = 128
                self.match(LineGrammarParser.TIE)
                self.state = 129
                localctx._CHORDMODALITY = self.match(LineGrammarParser.CHORDMODALITY)
                localctx.ctemplate = self.lc.construct_chord_template(localctx._tone.t, (None if localctx._CHORDMODALITY is None else localctx._CHORDMODALITY.text))
                pass
            elif token in [LineGrammarParser.CHORDNUMERAL]:
                self.enterOuterAlt(localctx, 2)
                self.state = 132
                localctx._CHORDNUMERAL = self.match(LineGrammarParser.CHORDNUMERAL)
                localctx.ctemplate = self.lc.construct_chord_template(None, (None if localctx._CHORDNUMERAL is None else localctx._CHORDNUMERAL.text))
                pass
            elif token in [LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS]:
                self.enterOuterAlt(localctx, 3)
                self.state = 134
                localctx._COMMON_DURATION_CHORD_NUMERAL_LETTERS = self.match(LineGrammarParser.COMMON_DURATION_CHORD_NUMERAL_LETTERS)
                localctx.ctemplate = self.lc.construct_chord_template(None, (None if localctx._COMMON_DURATION_CHORD_NUMERAL_LETTERS is None else localctx._COMMON_DURATION_CHORD_NUMERAL_LETTERS.text))
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class HarmonicTagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.ht = None
            self._tonality = None # TonalityContext
            self._chordTemplate = None # ChordTemplateContext

        def tonality(self):
            return self.getTypedRuleContext(LineGrammarParser.TonalityContext,0)


        def chordTemplate(self):
            return self.getTypedRuleContext(LineGrammarParser.ChordTemplateContext,0)


        def getRuleIndex(self):
            return LineGrammarParser.RULE_harmonicTag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHarmonicTag" ):
                listener.enterHarmonicTag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHarmonicTag" ):
                listener.exitHarmonicTag(self)




    def harmonicTag(self):

        localctx = LineGrammarParser.HarmonicTagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_harmonicTag)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(LineGrammarParser.T__6)
            self.state = 148
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [LineGrammarParser.COMMON_TONE_ALTERATION_LETTER, LineGrammarParser.TONELETTER]:
                self.state = 139
                localctx._tonality = self.tonality()
                self.state = 140
                self.match(LineGrammarParser.T__5)
                self.state = 141
                localctx._chordTemplate = self.chordTemplate()
                localctx.ht=self.lc.construct_harmonic_tag(localctx._tonality.tonal, localctx._chordTemplate.ctemplate)
                pass
            elif token in [LineGrammarParser.T__5]:
                self.state = 144
                self.match(LineGrammarParser.T__5)
                self.state = 145
                localctx._chordTemplate = self.chordTemplate()
                localctx.ht=self.lc.construct_harmonic_tag(None, localctx._chordTemplate.ctemplate)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 150
            self.match(LineGrammarParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





