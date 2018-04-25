# Generated from /Users/dpazel/PycharmProjects/music_rep_melody/resources/LineGrammar.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from structure.LineGrammar.core.line_constructor import LineConstructor
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\30")
        buf.write("\u00af\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\3\2\3\2")
        buf.write("\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3")
        buf.write("\t\3\n\3\n\3\13\3\13\3\f\6\fE\n\f\r\f\16\fF\3\r\3\r\3")
        buf.write("\16\3\16\3\17\6\17N\n\17\r\17\16\17O\3\17\3\17\3\20\3")
        buf.write("\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\5\24b\n\24\3\25\3\25\3\25\3\25\3\25\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\5\25\u0084\n\25\3\26\3\26\3\26\3")
        buf.write("\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\5\26\u00a0\n\26\3\27\3\27\3\27\3\27\3\27\3\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\3\27\5\27\u00ae\n\27\2\2\30\3")
        buf.write("\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16")
        buf.write("\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30\3\2\7")
        buf.write("\3\2\62;\4\2\13\13\"\"\4\2KKkk\n\2JJSSUVYZjjssuvyz\5\2")
        buf.write("CIccei\2\u00c5\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t")
        buf.write("\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3")
        buf.write("\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2")
        buf.write("\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2")
        buf.write("\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2")
        buf.write("\2\2-\3\2\2\2\3/\3\2\2\2\5\61\3\2\2\2\7\63\3\2\2\2\t\65")
        buf.write("\3\2\2\2\13\67\3\2\2\2\r9\3\2\2\2\17;\3\2\2\2\21=\3\2")
        buf.write("\2\2\23?\3\2\2\2\25A\3\2\2\2\27D\3\2\2\2\31H\3\2\2\2\33")
        buf.write("J\3\2\2\2\35M\3\2\2\2\37S\3\2\2\2!U\3\2\2\2#W\3\2\2\2")
        buf.write("%Y\3\2\2\2\'a\3\2\2\2)\u0083\3\2\2\2+\u009f\3\2\2\2-\u00ad")
        buf.write("\3\2\2\2/\60\7]\2\2\60\4\3\2\2\2\61\62\7_\2\2\62\6\3\2")
        buf.write("\2\2\63\64\7*\2\2\64\b\3\2\2\2\65\66\7.\2\2\66\n\3\2\2")
        buf.write("\2\678\7+\2\28\f\3\2\2\29:\7<\2\2:\16\3\2\2\2;<\7>\2\2")
        buf.write("<\20\3\2\2\2=>\7@\2\2>\22\3\2\2\2?@\7B\2\2@\24\3\2\2\2")
        buf.write("AB\7/\2\2B\26\3\2\2\2CE\t\2\2\2DC\3\2\2\2EF\3\2\2\2FD")
        buf.write("\3\2\2\2FG\3\2\2\2G\30\3\2\2\2HI\7}\2\2I\32\3\2\2\2JK")
        buf.write("\7\177\2\2K\34\3\2\2\2LN\t\3\2\2ML\3\2\2\2NO\3\2\2\2O")
        buf.write("M\3\2\2\2OP\3\2\2\2PQ\3\2\2\2QR\b\17\2\2R\36\3\2\2\2S")
        buf.write("T\7d\2\2T \3\2\2\2UV\t\4\2\2V\"\3\2\2\2WX\t\5\2\2X$\3")
        buf.write("\2\2\2YZ\t\6\2\2Z&\3\2\2\2[b\7d\2\2\\]\7d\2\2]b\7d\2\2")
        buf.write("^b\7%\2\2_`\7%\2\2`b\7%\2\2a[\3\2\2\2a\\\3\2\2\2a^\3\2")
        buf.write("\2\2a_\3\2\2\2b(\3\2\2\2cd\7O\2\2de\7c\2\2ef\7l\2\2fg")
        buf.write("\7q\2\2g\u0084\7t\2\2hi\7P\2\2ij\7c\2\2jk\7v\2\2kl\7w")
        buf.write("\2\2lm\7t\2\2mn\7c\2\2n\u0084\7n\2\2op\7O\2\2pq\7g\2\2")
        buf.write("qr\7n\2\2rs\7q\2\2st\7f\2\2tu\7k\2\2u\u0084\7e\2\2vw\7")
        buf.write("J\2\2wx\7c\2\2xy\7t\2\2yz\7o\2\2z{\7q\2\2{|\7p\2\2|}\7")
        buf.write("k\2\2}\u0084\7e\2\2~\177\7O\2\2\177\u0080\7k\2\2\u0080")
        buf.write("\u0081\7p\2\2\u0081\u0082\7q\2\2\u0082\u0084\7t\2\2\u0083")
        buf.write("c\3\2\2\2\u0083h\3\2\2\2\u0083o\3\2\2\2\u0083v\3\2\2\2")
        buf.write("\u0083~\3\2\2\2\u0084*\3\2\2\2\u0085\u0086\7K\2\2\u0086")
        buf.write("\u00a0\7K\2\2\u0087\u0088\7K\2\2\u0088\u0089\7K\2\2\u0089")
        buf.write("\u00a0\7K\2\2\u008a\u008b\7K\2\2\u008b\u00a0\7X\2\2\u008c")
        buf.write("\u00a0\7X\2\2\u008d\u008e\7X\2\2\u008e\u00a0\7K\2\2\u008f")
        buf.write("\u0090\7X\2\2\u0090\u0091\7K\2\2\u0091\u00a0\7K\2\2\u0092")
        buf.write("\u0093\7k\2\2\u0093\u00a0\7k\2\2\u0094\u0095\7k\2\2\u0095")
        buf.write("\u0096\7k\2\2\u0096\u00a0\7k\2\2\u0097\u0098\7k\2\2\u0098")
        buf.write("\u00a0\7x\2\2\u0099\u00a0\7x\2\2\u009a\u009b\7x\2\2\u009b")
        buf.write("\u00a0\7k\2\2\u009c\u009d\7x\2\2\u009d\u009e\7k\2\2\u009e")
        buf.write("\u00a0\7k\2\2\u009f\u0085\3\2\2\2\u009f\u0087\3\2\2\2")
        buf.write("\u009f\u008a\3\2\2\2\u009f\u008c\3\2\2\2\u009f\u008d\3")
        buf.write("\2\2\2\u009f\u008f\3\2\2\2\u009f\u0092\3\2\2\2\u009f\u0094")
        buf.write("\3\2\2\2\u009f\u0097\3\2\2\2\u009f\u0099\3\2\2\2\u009f")
        buf.write("\u009a\3\2\2\2\u009f\u009c\3\2\2\2\u00a0,\3\2\2\2\u00a1")
        buf.write("\u00a2\7O\2\2\u00a2\u00a3\7c\2\2\u00a3\u00ae\7l\2\2\u00a4")
        buf.write("\u00a5\7O\2\2\u00a5\u00a6\7k\2\2\u00a6\u00ae\7p\2\2\u00a7")
        buf.write("\u00a8\7C\2\2\u00a8\u00a9\7w\2\2\u00a9\u00ae\7i\2\2\u00aa")
        buf.write("\u00ab\7F\2\2\u00ab\u00ac\7k\2\2\u00ac\u00ae\7o\2\2\u00ad")
        buf.write("\u00a1\3\2\2\2\u00ad\u00a4\3\2\2\2\u00ad\u00a7\3\2\2\2")
        buf.write("\u00ad\u00aa\3\2\2\2\u00ae.\3\2\2\2\t\2FOa\u0083\u009f")
        buf.write("\u00ad\3\b\2\2")
        return buf.getvalue()


class LineGrammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    DOT = 9
    TIE = 10
    INT = 11
    LINEBEGIN = 12
    LINEEND = 13
    WS = 14
    COMMON_TONE_ALTERATION_LETTER = 15
    COMMON_DURATION_CHORD_NUMERAL_LETTERS = 16
    DURATIONLETTER = 17
    TONELETTER = 18
    ALTERATION = 19
    MODALITY = 20
    CHORDNUMERAL = 21
    CHORDMODALITY = 22

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'['", "']'", "'('", "','", "')'", "':'", "'<'", "'>'", "'@'", 
            "'-'", "'{'", "'}'", "'b'" ]

    symbolicNames = [ "<INVALID>",
            "DOT", "TIE", "INT", "LINEBEGIN", "LINEEND", "WS", "COMMON_TONE_ALTERATION_LETTER", 
            "COMMON_DURATION_CHORD_NUMERAL_LETTERS", "DURATIONLETTER", "TONELETTER", 
            "ALTERATION", "MODALITY", "CHORDNUMERAL", "CHORDMODALITY" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "DOT", "TIE", "INT", "LINEBEGIN", "LINEEND", "WS", 
                  "COMMON_TONE_ALTERATION_LETTER", "COMMON_DURATION_CHORD_NUMERAL_LETTERS", 
                  "DURATIONLETTER", "TONELETTER", "ALTERATION", "MODALITY", 
                  "CHORDNUMERAL", "CHORDMODALITY" ]

    grammarFileName = "LineGrammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


        self.lc = LineConstructor();
        self._notelist = list()


