# Generated from /Users/dpazel/PycharmProjects/music_rep_melody/resources/LineGrammar.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from structure.LineGrammar.core.line_constructor import LineConstructor
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\27")
        buf.write("\u0137\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\3\2\3\2\3\3\3\3\3")
        buf.write("\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n")
        buf.write("\3\13\3\13\3\f\6\fC\n\f\r\f\16\fD\3\r\3\r\3\16\3\16\3")
        buf.write("\17\6\17L\n\17\r\17\16\17M\3\17\3\17\3\20\3\20\3\21\3")
        buf.write("\21\3\22\3\22\3\22\3\22\3\22\5\22[\n\22\3\23\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\5\23}\n\23\3\24\3")
        buf.write("\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\5\24\u0099\n\24\3\25\3\25\3\25\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u00a7\n\25")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\5\26\u0136")
        buf.write("\n\26\2\2\27\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13")
        buf.write("\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26")
        buf.write("+\27\3\2\7\3\2\62;\4\2\13\13\"\"\4\2KKkk\n\2JJSSUVYZj")
        buf.write("jssuvyz\4\2CIci\2\u0184\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3")
        buf.write("\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2")
        buf.write("\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2")
        buf.write("\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2")
        buf.write("!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2")
        buf.write("\2+\3\2\2\2\3-\3\2\2\2\5/\3\2\2\2\7\61\3\2\2\2\t\63\3")
        buf.write("\2\2\2\13\65\3\2\2\2\r\67\3\2\2\2\179\3\2\2\2\21;\3\2")
        buf.write("\2\2\23=\3\2\2\2\25?\3\2\2\2\27B\3\2\2\2\31F\3\2\2\2\33")
        buf.write("H\3\2\2\2\35K\3\2\2\2\37Q\3\2\2\2!S\3\2\2\2#Z\3\2\2\2")
        buf.write("%|\3\2\2\2\'\u0098\3\2\2\2)\u00a6\3\2\2\2+\u0135\3\2\2")
        buf.write("\2-.\7]\2\2.\4\3\2\2\2/\60\7_\2\2\60\6\3\2\2\2\61\62\7")
        buf.write("*\2\2\62\b\3\2\2\2\63\64\7.\2\2\64\n\3\2\2\2\65\66\7+")
        buf.write("\2\2\66\f\3\2\2\2\678\7<\2\28\16\3\2\2\29:\7>\2\2:\20")
        buf.write("\3\2\2\2;<\7@\2\2<\22\3\2\2\2=>\7B\2\2>\24\3\2\2\2?@\7")
        buf.write("/\2\2@\26\3\2\2\2AC\t\2\2\2BA\3\2\2\2CD\3\2\2\2DB\3\2")
        buf.write("\2\2DE\3\2\2\2E\30\3\2\2\2FG\7}\2\2G\32\3\2\2\2HI\7\177")
        buf.write("\2\2I\34\3\2\2\2JL\t\3\2\2KJ\3\2\2\2LM\3\2\2\2MK\3\2\2")
        buf.write("\2MN\3\2\2\2NO\3\2\2\2OP\b\17\2\2P\36\3\2\2\2QR\t\4\2")
        buf.write("\2R \3\2\2\2ST\t\5\2\2T\"\3\2\2\2UV\7d\2\2V[\7d\2\2W[")
        buf.write("\7%\2\2XY\7%\2\2Y[\7%\2\2ZU\3\2\2\2ZW\3\2\2\2ZX\3\2\2")
        buf.write("\2[$\3\2\2\2\\]\7O\2\2]^\7c\2\2^_\7l\2\2_`\7q\2\2`}\7")
        buf.write("t\2\2ab\7P\2\2bc\7c\2\2cd\7v\2\2de\7w\2\2ef\7t\2\2fg\7")
        buf.write("c\2\2g}\7n\2\2hi\7O\2\2ij\7g\2\2jk\7n\2\2kl\7q\2\2lm\7")
        buf.write("f\2\2mn\7k\2\2n}\7e\2\2op\7J\2\2pq\7c\2\2qr\7t\2\2rs\7")
        buf.write("o\2\2st\7q\2\2tu\7p\2\2uv\7k\2\2v}\7e\2\2wx\7O\2\2xy\7")
        buf.write("k\2\2yz\7p\2\2z{\7q\2\2{}\7t\2\2|\\\3\2\2\2|a\3\2\2\2")
        buf.write("|h\3\2\2\2|o\3\2\2\2|w\3\2\2\2}&\3\2\2\2~\177\7K\2\2\177")
        buf.write("\u0099\7K\2\2\u0080\u0081\7K\2\2\u0081\u0082\7K\2\2\u0082")
        buf.write("\u0099\7K\2\2\u0083\u0084\7K\2\2\u0084\u0099\7X\2\2\u0085")
        buf.write("\u0099\7X\2\2\u0086\u0087\7X\2\2\u0087\u0099\7K\2\2\u0088")
        buf.write("\u0089\7X\2\2\u0089\u008a\7K\2\2\u008a\u0099\7K\2\2\u008b")
        buf.write("\u008c\7k\2\2\u008c\u0099\7k\2\2\u008d\u008e\7k\2\2\u008e")
        buf.write("\u008f\7k\2\2\u008f\u0099\7k\2\2\u0090\u0091\7k\2\2\u0091")
        buf.write("\u0099\7x\2\2\u0092\u0099\7x\2\2\u0093\u0094\7x\2\2\u0094")
        buf.write("\u0099\7k\2\2\u0095\u0096\7x\2\2\u0096\u0097\7k\2\2\u0097")
        buf.write("\u0099\7k\2\2\u0098~\3\2\2\2\u0098\u0080\3\2\2\2\u0098")
        buf.write("\u0083\3\2\2\2\u0098\u0085\3\2\2\2\u0098\u0086\3\2\2\2")
        buf.write("\u0098\u0088\3\2\2\2\u0098\u008b\3\2\2\2\u0098\u008d\3")
        buf.write("\2\2\2\u0098\u0090\3\2\2\2\u0098\u0092\3\2\2\2\u0098\u0093")
        buf.write("\3\2\2\2\u0098\u0095\3\2\2\2\u0099(\3\2\2\2\u009a\u009b")
        buf.write("\7O\2\2\u009b\u009c\7c\2\2\u009c\u00a7\7l\2\2\u009d\u009e")
        buf.write("\7O\2\2\u009e\u009f\7k\2\2\u009f\u00a7\7p\2\2\u00a0\u00a1")
        buf.write("\7C\2\2\u00a1\u00a2\7w\2\2\u00a2\u00a7\7i\2\2\u00a3\u00a4")
        buf.write("\7F\2\2\u00a4\u00a5\7k\2\2\u00a5\u00a7\7o\2\2\u00a6\u009a")
        buf.write("\3\2\2\2\u00a6\u009d\3\2\2\2\u00a6\u00a0\3\2\2\2\u00a6")
        buf.write("\u00a3\3\2\2\2\u00a7*\3\2\2\2\u00a8\u0136\t\6\2\2\u00a9")
        buf.write("\u00aa\7E\2\2\u00aa\u0136\7d\2\2\u00ab\u00ac\7F\2\2\u00ac")
        buf.write("\u0136\7d\2\2\u00ad\u00ae\7G\2\2\u00ae\u0136\7d\2\2\u00af")
        buf.write("\u00b0\7H\2\2\u00b0\u0136\7d\2\2\u00b1\u00b2\7I\2\2\u00b2")
        buf.write("\u0136\7d\2\2\u00b3\u00b4\7C\2\2\u00b4\u0136\7d\2\2\u00b5")
        buf.write("\u00b6\7D\2\2\u00b6\u0136\7d\2\2\u00b7\u00b8\7e\2\2\u00b8")
        buf.write("\u0136\7d\2\2\u00b9\u00ba\7f\2\2\u00ba\u0136\7d\2\2\u00bb")
        buf.write("\u00bc\7g\2\2\u00bc\u0136\7d\2\2\u00bd\u00be\7h\2\2\u00be")
        buf.write("\u0136\7d\2\2\u00bf\u00c0\7i\2\2\u00c0\u0136\7d\2\2\u00c1")
        buf.write("\u00c2\7c\2\2\u00c2\u0136\7d\2\2\u00c3\u00c4\7d\2\2\u00c4")
        buf.write("\u0136\7d\2\2\u00c5\u00c6\7E\2\2\u00c6\u00c7\7d\2\2\u00c7")
        buf.write("\u0136\7d\2\2\u00c8\u00c9\7F\2\2\u00c9\u00ca\7d\2\2\u00ca")
        buf.write("\u0136\7d\2\2\u00cb\u00cc\7G\2\2\u00cc\u00cd\7d\2\2\u00cd")
        buf.write("\u0136\7d\2\2\u00ce\u00cf\7H\2\2\u00cf\u00d0\7d\2\2\u00d0")
        buf.write("\u0136\7d\2\2\u00d1\u00d2\7I\2\2\u00d2\u00d3\7d\2\2\u00d3")
        buf.write("\u0136\7d\2\2\u00d4\u00d5\7C\2\2\u00d5\u00d6\7d\2\2\u00d6")
        buf.write("\u0136\7d\2\2\u00d7\u00d8\7D\2\2\u00d8\u00d9\7d\2\2\u00d9")
        buf.write("\u0136\7d\2\2\u00da\u00db\7e\2\2\u00db\u00dc\7d\2\2\u00dc")
        buf.write("\u0136\7d\2\2\u00dd\u00de\7f\2\2\u00de\u00df\7d\2\2\u00df")
        buf.write("\u0136\7d\2\2\u00e0\u00e1\7g\2\2\u00e1\u00e2\7d\2\2\u00e2")
        buf.write("\u0136\7d\2\2\u00e3\u00e4\7h\2\2\u00e4\u00e5\7d\2\2\u00e5")
        buf.write("\u0136\7d\2\2\u00e6\u00e7\7i\2\2\u00e7\u00e8\7d\2\2\u00e8")
        buf.write("\u0136\7d\2\2\u00e9\u00ea\7c\2\2\u00ea\u00eb\7d\2\2\u00eb")
        buf.write("\u0136\7d\2\2\u00ec\u00ed\7d\2\2\u00ed\u00ee\7d\2\2\u00ee")
        buf.write("\u0136\7d\2\2\u00ef\u00f0\7E\2\2\u00f0\u0136\7%\2\2\u00f1")
        buf.write("\u00f2\7F\2\2\u00f2\u0136\7%\2\2\u00f3\u00f4\7G\2\2\u00f4")
        buf.write("\u0136\7%\2\2\u00f5\u00f6\7H\2\2\u00f6\u0136\7%\2\2\u00f7")
        buf.write("\u00f8\7I\2\2\u00f8\u0136\7%\2\2\u00f9\u00fa\7C\2\2\u00fa")
        buf.write("\u0136\7%\2\2\u00fb\u00fc\7D\2\2\u00fc\u0136\7%\2\2\u00fd")
        buf.write("\u00fe\7e\2\2\u00fe\u0136\7%\2\2\u00ff\u0100\7f\2\2\u0100")
        buf.write("\u0136\7%\2\2\u0101\u0102\7g\2\2\u0102\u0136\7%\2\2\u0103")
        buf.write("\u0104\7h\2\2\u0104\u0136\7%\2\2\u0105\u0106\7i\2\2\u0106")
        buf.write("\u0136\7%\2\2\u0107\u0108\7c\2\2\u0108\u0136\7%\2\2\u0109")
        buf.write("\u010a\7d\2\2\u010a\u0136\7%\2\2\u010b\u010c\7E\2\2\u010c")
        buf.write("\u010d\7%\2\2\u010d\u0136\7%\2\2\u010e\u010f\7F\2\2\u010f")
        buf.write("\u0110\7%\2\2\u0110\u0136\7%\2\2\u0111\u0112\7G\2\2\u0112")
        buf.write("\u0113\7%\2\2\u0113\u0136\7%\2\2\u0114\u0115\7H\2\2\u0115")
        buf.write("\u0116\7%\2\2\u0116\u0136\7%\2\2\u0117\u0118\7I\2\2\u0118")
        buf.write("\u0119\7%\2\2\u0119\u0136\7%\2\2\u011a\u011b\7C\2\2\u011b")
        buf.write("\u011c\7%\2\2\u011c\u0136\7%\2\2\u011d\u011e\7D\2\2\u011e")
        buf.write("\u011f\7%\2\2\u011f\u0136\7%\2\2\u0120\u0121\7e\2\2\u0121")
        buf.write("\u0122\7%\2\2\u0122\u0136\7%\2\2\u0123\u0124\7f\2\2\u0124")
        buf.write("\u0125\7%\2\2\u0125\u0136\7%\2\2\u0126\u0127\7g\2\2\u0127")
        buf.write("\u0128\7%\2\2\u0128\u0136\7%\2\2\u0129\u012a\7h\2\2\u012a")
        buf.write("\u012b\7%\2\2\u012b\u0136\7%\2\2\u012c\u012d\7i\2\2\u012d")
        buf.write("\u012e\7%\2\2\u012e\u0136\7%\2\2\u012f\u0130\7c\2\2\u0130")
        buf.write("\u0131\7%\2\2\u0131\u0136\7%\2\2\u0132\u0133\7d\2\2\u0133")
        buf.write("\u0134\7%\2\2\u0134\u0136\7%\2\2\u0135\u00a8\3\2\2\2\u0135")
        buf.write("\u00a9\3\2\2\2\u0135\u00ab\3\2\2\2\u0135\u00ad\3\2\2\2")
        buf.write("\u0135\u00af\3\2\2\2\u0135\u00b1\3\2\2\2\u0135\u00b3\3")
        buf.write("\2\2\2\u0135\u00b5\3\2\2\2\u0135\u00b7\3\2\2\2\u0135\u00b9")
        buf.write("\3\2\2\2\u0135\u00bb\3\2\2\2\u0135\u00bd\3\2\2\2\u0135")
        buf.write("\u00bf\3\2\2\2\u0135\u00c1\3\2\2\2\u0135\u00c3\3\2\2\2")
        buf.write("\u0135\u00c5\3\2\2\2\u0135\u00c8\3\2\2\2\u0135\u00cb\3")
        buf.write("\2\2\2\u0135\u00ce\3\2\2\2\u0135\u00d1\3\2\2\2\u0135\u00d4")
        buf.write("\3\2\2\2\u0135\u00d7\3\2\2\2\u0135\u00da\3\2\2\2\u0135")
        buf.write("\u00dd\3\2\2\2\u0135\u00e0\3\2\2\2\u0135\u00e3\3\2\2\2")
        buf.write("\u0135\u00e6\3\2\2\2\u0135\u00e9\3\2\2\2\u0135\u00ec\3")
        buf.write("\2\2\2\u0135\u00ef\3\2\2\2\u0135\u00f1\3\2\2\2\u0135\u00f3")
        buf.write("\3\2\2\2\u0135\u00f5\3\2\2\2\u0135\u00f7\3\2\2\2\u0135")
        buf.write("\u00f9\3\2\2\2\u0135\u00fb\3\2\2\2\u0135\u00fd\3\2\2\2")
        buf.write("\u0135\u00ff\3\2\2\2\u0135\u0101\3\2\2\2\u0135\u0103\3")
        buf.write("\2\2\2\u0135\u0105\3\2\2\2\u0135\u0107\3\2\2\2\u0135\u0109")
        buf.write("\3\2\2\2\u0135\u010b\3\2\2\2\u0135\u010e\3\2\2\2\u0135")
        buf.write("\u0111\3\2\2\2\u0135\u0114\3\2\2\2\u0135\u0117\3\2\2\2")
        buf.write("\u0135\u011a\3\2\2\2\u0135\u011d\3\2\2\2\u0135\u0120\3")
        buf.write("\2\2\2\u0135\u0123\3\2\2\2\u0135\u0126\3\2\2\2\u0135\u0129")
        buf.write("\3\2\2\2\u0135\u012c\3\2\2\2\u0135\u012f\3\2\2\2\u0135")
        buf.write("\u0132\3\2\2\2\u0136,\3\2\2\2\n\2DMZ|\u0098\u00a6\u0135")
        buf.write("\3\b\2\2")
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
    COMMON_DURATION_CHORD_NUMERAL_LETTERS = 15
    DURATIONLETTER = 16
    ALTERATION = 17
    MODALITY = 18
    CHORDNUMERAL = 19
    CHORDMODALITY = 20
    NOTELETTERS = 21

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'['", "']'", "'('", "','", "')'", "':'", "'<'", "'>'", "'@'", 
            "'-'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>",
            "DOT", "TIE", "INT", "LINEBEGIN", "LINEEND", "WS", "COMMON_DURATION_CHORD_NUMERAL_LETTERS", 
            "DURATIONLETTER", "ALTERATION", "MODALITY", "CHORDNUMERAL", 
            "CHORDMODALITY", "NOTELETTERS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "DOT", "TIE", "INT", "LINEBEGIN", "LINEEND", "WS", 
                  "COMMON_DURATION_CHORD_NUMERAL_LETTERS", "DURATIONLETTER", 
                  "ALTERATION", "MODALITY", "CHORDNUMERAL", "CHORDMODALITY", 
                  "NOTELETTERS" ]

    grammarFileName = "LineGrammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


        self.lc = LineConstructor();
        self._notelist = list()


