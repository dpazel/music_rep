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
        buf.write("\u024d\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7")
        buf.write("\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r\6\r")
        buf.write("K\n\r\r\r\16\rL\3\16\3\16\3\17\3\17\3\20\6\20T\n\20\r")
        buf.write("\20\16\20U\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\23")
        buf.write("\3\23\3\23\5\23c\n\23\3\24\3\24\6\24g\n\24\r\24\16\24")
        buf.write("h\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u017a\n")
        buf.write("\25\3\26\3\26\5\26\u017e\n\26\3\27\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27")
        buf.write("\u019a\n\27\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3")
        buf.write("\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\30\3\30\5\30\u01bc\n\30\3\31\3\31\3\31\3\31\3\31\3")
        buf.write("\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\5\31\u024c\n\31\2\2\32\3\3\5")
        buf.write("\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33")
        buf.write("\17\35\20\37\21!\22#\23%\24\'\2)\2+\25-\26/\27\61\30\3")
        buf.write("\2\t\3\2\62;\4\2\13\13\"\"\4\2KKkk\n\2JJSSUVYZjjssuvy")
        buf.write("z\4\2C\\c|\4\2CIci\4\2TTtt\2\u02b4\2\3\3\2\2\2\2\5\3\2")
        buf.write("\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2")
        buf.write("\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2")
        buf.write("\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37")
        buf.write("\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2+\3\2\2\2\2")
        buf.write("-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\3\63\3\2\2\2\5\65\3")
        buf.write("\2\2\2\7\67\3\2\2\2\t9\3\2\2\2\13;\3\2\2\2\r=\3\2\2\2")
        buf.write("\17?\3\2\2\2\21A\3\2\2\2\23C\3\2\2\2\25E\3\2\2\2\27G\3")
        buf.write("\2\2\2\31J\3\2\2\2\33N\3\2\2\2\35P\3\2\2\2\37S\3\2\2\2")
        buf.write("!Y\3\2\2\2#[\3\2\2\2%b\3\2\2\2\'d\3\2\2\2)\u0179\3\2\2")
        buf.write("\2+\u017d\3\2\2\2-\u0199\3\2\2\2/\u01bb\3\2\2\2\61\u024b")
        buf.write("\3\2\2\2\63\64\7]\2\2\64\4\3\2\2\2\65\66\7_\2\2\66\6\3")
        buf.write("\2\2\2\678\7*\2\28\b\3\2\2\29:\7.\2\2:\n\3\2\2\2;<\7+")
        buf.write("\2\2<\f\3\2\2\2=>\7<\2\2>\16\3\2\2\2?@\7\61\2\2@\20\3")
        buf.write("\2\2\2AB\7>\2\2B\22\3\2\2\2CD\7@\2\2D\24\3\2\2\2EF\7B")
        buf.write("\2\2F\26\3\2\2\2GH\7/\2\2H\30\3\2\2\2IK\t\2\2\2JI\3\2")
        buf.write("\2\2KL\3\2\2\2LJ\3\2\2\2LM\3\2\2\2M\32\3\2\2\2NO\7}\2")
        buf.write("\2O\34\3\2\2\2PQ\7\177\2\2Q\36\3\2\2\2RT\t\3\2\2SR\3\2")
        buf.write("\2\2TU\3\2\2\2US\3\2\2\2UV\3\2\2\2VW\3\2\2\2WX\b\20\2")
        buf.write("\2X \3\2\2\2YZ\t\4\2\2Z\"\3\2\2\2[\\\t\5\2\2\\$\3\2\2")
        buf.write("\2]^\7d\2\2^c\7d\2\2_c\7%\2\2`a\7%\2\2ac\7%\2\2b]\3\2")
        buf.write("\2\2b_\3\2\2\2b`\3\2\2\2c&\3\2\2\2df\7#\2\2eg\t\6\2\2")
        buf.write("fe\3\2\2\2gh\3\2\2\2hf\3\2\2\2hi\3\2\2\2i(\3\2\2\2jk\7")
        buf.write("O\2\2kl\7c\2\2lm\7l\2\2mn\7q\2\2n\u017a\7t\2\2op\7P\2")
        buf.write("\2pq\7c\2\2qr\7v\2\2rs\7w\2\2st\7t\2\2tu\7c\2\2u\u017a")
        buf.write("\7n\2\2vw\7O\2\2wx\7g\2\2xy\7n\2\2yz\7q\2\2z{\7f\2\2{")
        buf.write("|\7k\2\2|\u017a\7e\2\2}~\7J\2\2~\177\7c\2\2\177\u0080")
        buf.write("\7t\2\2\u0080\u0081\7o\2\2\u0081\u0082\7q\2\2\u0082\u0083")
        buf.write("\7p\2\2\u0083\u0084\7k\2\2\u0084\u017a\7e\2\2\u0085\u0086")
        buf.write("\7O\2\2\u0086\u0087\7k\2\2\u0087\u0088\7p\2\2\u0088\u0089")
        buf.write("\7q\2\2\u0089\u017a\7t\2\2\u008a\u008b\7P\2\2\u008b\u008c")
        buf.write("\7c\2\2\u008c\u008d\7v\2\2\u008d\u008e\7w\2\2\u008e\u008f")
        buf.write("\7t\2\2\u008f\u0090\7c\2\2\u0090\u0091\7n\2\2\u0091\u0092")
        buf.write("\7O\2\2\u0092\u0093\7k\2\2\u0093\u0094\7p\2\2\u0094\u0095")
        buf.write("\7q\2\2\u0095\u017a\7t\2\2\u0096\u0097\7O\2\2\u0097\u0098")
        buf.write("\7g\2\2\u0098\u0099\7n\2\2\u0099\u009a\7q\2\2\u009a\u009b")
        buf.write("\7f\2\2\u009b\u009c\7k\2\2\u009c\u009d\7e\2\2\u009d\u009e")
        buf.write("\7O\2\2\u009e\u009f\7k\2\2\u009f\u00a0\7p\2\2\u00a0\u00a1")
        buf.write("\7q\2\2\u00a1\u017a\7t\2\2\u00a2\u00a3\7J\2\2\u00a3\u00a4")
        buf.write("\7c\2\2\u00a4\u00a5\7t\2\2\u00a5\u00a6\7o\2\2\u00a6\u00a7")
        buf.write("\7q\2\2\u00a7\u00a8\7p\2\2\u00a8\u00a9\7k\2\2\u00a9\u00aa")
        buf.write("\7e\2\2\u00aa\u00ab\7O\2\2\u00ab\u00ac\7k\2\2\u00ac\u00ad")
        buf.write("\7p\2\2\u00ad\u00ae\7q\2\2\u00ae\u017a\7t\2\2\u00af\u00b0")
        buf.write("\7J\2\2\u00b0\u00b1\7c\2\2\u00b1\u00b2\7t\2\2\u00b2\u00b3")
        buf.write("\7o\2\2\u00b3\u00b4\7q\2\2\u00b4\u00b5\7p\2\2\u00b5\u00b6")
        buf.write("\7k\2\2\u00b6\u00b7\7e\2\2\u00b7\u00b8\7O\2\2\u00b8\u00b9")
        buf.write("\7c\2\2\u00b9\u00ba\7l\2\2\u00ba\u00bb\7q\2\2\u00bb\u017a")
        buf.write("\7t\2\2\u00bc\u00bd\7K\2\2\u00bd\u00be\7q\2\2\u00be\u00bf")
        buf.write("\7p\2\2\u00bf\u00c0\7k\2\2\u00c0\u00c1\7c\2\2\u00c1\u017a")
        buf.write("\7p\2\2\u00c2\u00c3\7F\2\2\u00c3\u00c4\7q\2\2\u00c4\u00c5")
        buf.write("\7t\2\2\u00c5\u00c6\7k\2\2\u00c6\u00c7\7c\2\2\u00c7\u017a")
        buf.write("\7p\2\2\u00c8\u00c9\7R\2\2\u00c9\u00ca\7j\2\2\u00ca\u00cb")
        buf.write("\7t\2\2\u00cb\u00cc\7{\2\2\u00cc\u00cd\7i\2\2\u00cd\u00ce")
        buf.write("\7k\2\2\u00ce\u00cf\7c\2\2\u00cf\u017a\7p\2\2\u00d0\u00d1")
        buf.write("\7N\2\2\u00d1\u00d2\7{\2\2\u00d2\u00d3\7f\2\2\u00d3\u00d4")
        buf.write("\7k\2\2\u00d4\u00d5\7c\2\2\u00d5\u017a\7p\2\2\u00d6\u00d7")
        buf.write("\7O\2\2\u00d7\u00d8\7{\2\2\u00d8\u00d9\7z\2\2\u00d9\u00da")
        buf.write("\7q\2\2\u00da\u00db\7n\2\2\u00db\u00dc\7{\2\2\u00dc\u00dd")
        buf.write("\7f\2\2\u00dd\u00de\7k\2\2\u00de\u00df\7c\2\2\u00df\u017a")
        buf.write("\7p\2\2\u00e0\u00e1\7C\2\2\u00e1\u00e2\7g\2\2\u00e2\u00e3")
        buf.write("\7q\2\2\u00e3\u00e4\7n\2\2\u00e4\u00e5\7k\2\2\u00e5\u00e6")
        buf.write("\7c\2\2\u00e6\u017a\7p\2\2\u00e7\u00e8\7N\2\2\u00e8\u00e9")
        buf.write("\7q\2\2\u00e9\u00ea\7e\2\2\u00ea\u00eb\7t\2\2\u00eb\u00ec")
        buf.write("\7k\2\2\u00ec\u00ed\7c\2\2\u00ed\u017a\7p\2\2\u00ee\u00ef")
        buf.write("\7Y\2\2\u00ef\u00f0\7j\2\2\u00f0\u00f1\7q\2\2\u00f1\u00f2")
        buf.write("\7n\2\2\u00f2\u00f3\7g\2\2\u00f3\u00f4\7V\2\2\u00f4\u00f5")
        buf.write("\7q\2\2\u00f5\u00f6\7p\2\2\u00f6\u017a\7g\2\2\u00f7\u00f8")
        buf.write("\7O\2\2\u00f8\u00f9\7c\2\2\u00f9\u00fa\7l\2\2\u00fa\u00fb")
        buf.write("\7q\2\2\u00fb\u00fc\7t\2\2\u00fc\u00fd\7R\2\2\u00fd\u00fe")
        buf.write("\7g\2\2\u00fe\u00ff\7p\2\2\u00ff\u0100\7v\2\2\u0100\u0101")
        buf.write("\7c\2\2\u0101\u0102\7v\2\2\u0102\u0103\7q\2\2\u0103\u0104")
        buf.write("\7p\2\2\u0104\u0105\7k\2\2\u0105\u017a\7e\2\2\u0106\u0107")
        buf.write("\7G\2\2\u0107\u0108\7i\2\2\u0108\u0109\7{\2\2\u0109\u010a")
        buf.write("\7r\2\2\u010a\u010b\7v\2\2\u010b\u010c\7k\2\2\u010c\u010d")
        buf.write("\7c\2\2\u010d\u010e\7p\2\2\u010e\u010f\7R\2\2\u010f\u0110")
        buf.write("\7g\2\2\u0110\u0111\7p\2\2\u0111\u0112\7v\2\2\u0112\u0113")
        buf.write("\7c\2\2\u0113\u0114\7v\2\2\u0114\u0115\7q\2\2\u0115\u0116")
        buf.write("\7p\2\2\u0116\u0117\7k\2\2\u0117\u017a\7e\2\2\u0118\u0119")
        buf.write("\7O\2\2\u0119\u011a\7k\2\2\u011a\u011b\7p\2\2\u011b\u011c")
        buf.write("\7q\2\2\u011c\u011d\7t\2\2\u011d\u011e\7D\2\2\u011e\u011f")
        buf.write("\7n\2\2\u011f\u0120\7w\2\2\u0120\u0121\7g\2\2\u0121\u0122")
        buf.write("\7u\2\2\u0122\u0123\7R\2\2\u0123\u0124\7g\2\2\u0124\u0125")
        buf.write("\7p\2\2\u0125\u0126\7v\2\2\u0126\u0127\7c\2\2\u0127\u0128")
        buf.write("\7v\2\2\u0128\u0129\7q\2\2\u0129\u012a\7p\2\2\u012a\u012b")
        buf.write("\7k\2\2\u012b\u017a\7e\2\2\u012c\u012d\7O\2\2\u012d\u012e")
        buf.write("\7c\2\2\u012e\u012f\7l\2\2\u012f\u0130\7q\2\2\u0130\u0131")
        buf.write("\7t\2\2\u0131\u0132\7D\2\2\u0132\u0133\7n\2\2\u0133\u0134")
        buf.write("\7w\2\2\u0134\u0135\7g\2\2\u0135\u0136\7u\2\2\u0136\u0137")
        buf.write("\7R\2\2\u0137\u0138\7g\2\2\u0138\u0139\7p\2\2\u0139\u013a")
        buf.write("\7v\2\2\u013a\u013b\7c\2\2\u013b\u013c\7v\2\2\u013c\u013d")
        buf.write("\7q\2\2\u013d\u013e\7p\2\2\u013e\u013f\7k\2\2\u013f\u017a")
        buf.write("\7e\2\2\u0140\u0141\7O\2\2\u0141\u0142\7k\2\2\u0142\u0143")
        buf.write("\7p\2\2\u0143\u0144\7q\2\2\u0144\u0145\7t\2\2\u0145\u0146")
        buf.write("\7R\2\2\u0146\u0147\7g\2\2\u0147\u0148\7p\2\2\u0148\u0149")
        buf.write("\7v\2\2\u0149\u014a\7c\2\2\u014a\u014b\7v\2\2\u014b\u014c")
        buf.write("\7q\2\2\u014c\u014d\7p\2\2\u014d\u014e\7k\2\2\u014e\u017a")
        buf.write("\7e\2\2\u014f\u0150\7J\2\2\u0150\u0151\7Y\2\2\u0151\u0152")
        buf.write("\7Q\2\2\u0152\u0153\7e\2\2\u0153\u0154\7v\2\2\u0154\u0155")
        buf.write("\7c\2\2\u0155\u0156\7v\2\2\u0156\u0157\7q\2\2\u0157\u0158")
        buf.write("\7p\2\2\u0158\u0159\7k\2\2\u0159\u017a\7e\2\2\u015a\u015b")
        buf.write("\7Y\2\2\u015b\u015c\7J\2\2\u015c\u015d\7Q\2\2\u015d\u015e")
        buf.write("\7e\2\2\u015e\u015f\7v\2\2\u015f\u0160\7c\2\2\u0160\u0161")
        buf.write("\7v\2\2\u0161\u0162\7q\2\2\u0162\u0163\7p\2\2\u0163\u0164")
        buf.write("\7k\2\2\u0164\u017a\7e\2\2\u0165\u0166\7O\2\2\u0166\u0167")
        buf.write("\7c\2\2\u0167\u0168\7l\2\2\u0168\u0169\7q\2\2\u0169\u016a")
        buf.write("\7t\2\2\u016a\u016b\7D\2\2\u016b\u016c\7n\2\2\u016c\u016d")
        buf.write("\7w\2\2\u016d\u016e\7g\2\2\u016e\u017a\7u\2\2\u016f\u0170")
        buf.write("\7O\2\2\u0170\u0171\7k\2\2\u0171\u0172\7p\2\2\u0172\u0173")
        buf.write("\7q\2\2\u0173\u0174\7t\2\2\u0174\u0175\7D\2\2\u0175\u0176")
        buf.write("\7n\2\2\u0176\u0177\7w\2\2\u0177\u0178\7g\2\2\u0178\u017a")
        buf.write("\7u\2\2\u0179j\3\2\2\2\u0179o\3\2\2\2\u0179v\3\2\2\2\u0179")
        buf.write("}\3\2\2\2\u0179\u0085\3\2\2\2\u0179\u008a\3\2\2\2\u0179")
        buf.write("\u0096\3\2\2\2\u0179\u00a2\3\2\2\2\u0179\u00af\3\2\2\2")
        buf.write("\u0179\u00bc\3\2\2\2\u0179\u00c2\3\2\2\2\u0179\u00c8\3")
        buf.write("\2\2\2\u0179\u00d0\3\2\2\2\u0179\u00d6\3\2\2\2\u0179\u00e0")
        buf.write("\3\2\2\2\u0179\u00e7\3\2\2\2\u0179\u00ee\3\2\2\2\u0179")
        buf.write("\u00f7\3\2\2\2\u0179\u0106\3\2\2\2\u0179\u0118\3\2\2\2")
        buf.write("\u0179\u012c\3\2\2\2\u0179\u0140\3\2\2\2\u0179\u014f\3")
        buf.write("\2\2\2\u0179\u015a\3\2\2\2\u0179\u0165\3\2\2\2\u0179\u016f")
        buf.write("\3\2\2\2\u017a*\3\2\2\2\u017b\u017e\5)\25\2\u017c\u017e")
        buf.write("\5\'\24\2\u017d\u017b\3\2\2\2\u017d\u017c\3\2\2\2\u017e")
        buf.write(",\3\2\2\2\u017f\u0180\7K\2\2\u0180\u019a\7K\2\2\u0181")
        buf.write("\u0182\7K\2\2\u0182\u0183\7K\2\2\u0183\u019a\7K\2\2\u0184")
        buf.write("\u0185\7K\2\2\u0185\u019a\7X\2\2\u0186\u019a\7X\2\2\u0187")
        buf.write("\u0188\7X\2\2\u0188\u019a\7K\2\2\u0189\u018a\7X\2\2\u018a")
        buf.write("\u018b\7K\2\2\u018b\u019a\7K\2\2\u018c\u018d\7k\2\2\u018d")
        buf.write("\u019a\7k\2\2\u018e\u018f\7k\2\2\u018f\u0190\7k\2\2\u0190")
        buf.write("\u019a\7k\2\2\u0191\u0192\7k\2\2\u0192\u019a\7x\2\2\u0193")
        buf.write("\u019a\7x\2\2\u0194\u0195\7x\2\2\u0195\u019a\7k\2\2\u0196")
        buf.write("\u0197\7x\2\2\u0197\u0198\7k\2\2\u0198\u019a\7k\2\2\u0199")
        buf.write("\u017f\3\2\2\2\u0199\u0181\3\2\2\2\u0199\u0184\3\2\2\2")
        buf.write("\u0199\u0186\3\2\2\2\u0199\u0187\3\2\2\2\u0199\u0189\3")
        buf.write("\2\2\2\u0199\u018c\3\2\2\2\u0199\u018e\3\2\2\2\u0199\u0191")
        buf.write("\3\2\2\2\u0199\u0193\3\2\2\2\u0199\u0194\3\2\2\2\u0199")
        buf.write("\u0196\3\2\2\2\u019a.\3\2\2\2\u019b\u019c\7O\2\2\u019c")
        buf.write("\u019d\7c\2\2\u019d\u019e\7l\2\2\u019e\u01bc\79\2\2\u019f")
        buf.write("\u01a0\7O\2\2\u01a0\u01a1\7k\2\2\u01a1\u01a2\7p\2\2\u01a2")
        buf.write("\u01bc\79\2\2\u01a3\u01a4\7F\2\2\u01a4\u01a5\7q\2\2\u01a5")
        buf.write("\u01a6\7o\2\2\u01a6\u01bc\79\2\2\u01a7\u01a8\7O\2\2\u01a8")
        buf.write("\u01a9\7c\2\2\u01a9\u01bc\7l\2\2\u01aa\u01ab\7O\2\2\u01ab")
        buf.write("\u01ac\7k\2\2\u01ac\u01bc\7p\2\2\u01ad\u01ae\7C\2\2\u01ae")
        buf.write("\u01af\7w\2\2\u01af\u01bc\7i\2\2\u01b0\u01b1\7F\2\2\u01b1")
        buf.write("\u01b2\7k\2\2\u01b2\u01bc\7o\2\2\u01b3\u01b4\7J\2\2\u01b4")
        buf.write("\u01b5\7c\2\2\u01b5\u01b6\7n\2\2\u01b6\u01b7\7h\2\2\u01b7")
        buf.write("\u01b8\7F\2\2\u01b8\u01b9\7k\2\2\u01b9\u01ba\7o\2\2\u01ba")
        buf.write("\u01bc\79\2\2\u01bb\u019b\3\2\2\2\u01bb\u019f\3\2\2\2")
        buf.write("\u01bb\u01a3\3\2\2\2\u01bb\u01a7\3\2\2\2\u01bb\u01aa\3")
        buf.write("\2\2\2\u01bb\u01ad\3\2\2\2\u01bb\u01b0\3\2\2\2\u01bb\u01b3")
        buf.write("\3\2\2\2\u01bc\60\3\2\2\2\u01bd\u024c\t\7\2\2\u01be\u01bf")
        buf.write("\7E\2\2\u01bf\u024c\7d\2\2\u01c0\u01c1\7F\2\2\u01c1\u024c")
        buf.write("\7d\2\2\u01c2\u01c3\7G\2\2\u01c3\u024c\7d\2\2\u01c4\u01c5")
        buf.write("\7H\2\2\u01c5\u024c\7d\2\2\u01c6\u01c7\7I\2\2\u01c7\u024c")
        buf.write("\7d\2\2\u01c8\u01c9\7C\2\2\u01c9\u024c\7d\2\2\u01ca\u01cb")
        buf.write("\7D\2\2\u01cb\u024c\7d\2\2\u01cc\u01cd\7e\2\2\u01cd\u024c")
        buf.write("\7d\2\2\u01ce\u01cf\7f\2\2\u01cf\u024c\7d\2\2\u01d0\u01d1")
        buf.write("\7g\2\2\u01d1\u024c\7d\2\2\u01d2\u01d3\7h\2\2\u01d3\u024c")
        buf.write("\7d\2\2\u01d4\u01d5\7i\2\2\u01d5\u024c\7d\2\2\u01d6\u01d7")
        buf.write("\7c\2\2\u01d7\u024c\7d\2\2\u01d8\u01d9\7d\2\2\u01d9\u024c")
        buf.write("\7d\2\2\u01da\u01db\7E\2\2\u01db\u01dc\7d\2\2\u01dc\u024c")
        buf.write("\7d\2\2\u01dd\u01de\7F\2\2\u01de\u01df\7d\2\2\u01df\u024c")
        buf.write("\7d\2\2\u01e0\u01e1\7G\2\2\u01e1\u01e2\7d\2\2\u01e2\u024c")
        buf.write("\7d\2\2\u01e3\u01e4\7H\2\2\u01e4\u01e5\7d\2\2\u01e5\u024c")
        buf.write("\7d\2\2\u01e6\u01e7\7I\2\2\u01e7\u01e8\7d\2\2\u01e8\u024c")
        buf.write("\7d\2\2\u01e9\u01ea\7C\2\2\u01ea\u01eb\7d\2\2\u01eb\u024c")
        buf.write("\7d\2\2\u01ec\u01ed\7D\2\2\u01ed\u01ee\7d\2\2\u01ee\u024c")
        buf.write("\7d\2\2\u01ef\u01f0\7e\2\2\u01f0\u01f1\7d\2\2\u01f1\u024c")
        buf.write("\7d\2\2\u01f2\u01f3\7f\2\2\u01f3\u01f4\7d\2\2\u01f4\u024c")
        buf.write("\7d\2\2\u01f5\u01f6\7g\2\2\u01f6\u01f7\7d\2\2\u01f7\u024c")
        buf.write("\7d\2\2\u01f8\u01f9\7h\2\2\u01f9\u01fa\7d\2\2\u01fa\u024c")
        buf.write("\7d\2\2\u01fb\u01fc\7i\2\2\u01fc\u01fd\7d\2\2\u01fd\u024c")
        buf.write("\7d\2\2\u01fe\u01ff\7c\2\2\u01ff\u0200\7d\2\2\u0200\u024c")
        buf.write("\7d\2\2\u0201\u0202\7d\2\2\u0202\u0203\7d\2\2\u0203\u024c")
        buf.write("\7d\2\2\u0204\u0205\7E\2\2\u0205\u024c\7%\2\2\u0206\u0207")
        buf.write("\7F\2\2\u0207\u024c\7%\2\2\u0208\u0209\7G\2\2\u0209\u024c")
        buf.write("\7%\2\2\u020a\u020b\7H\2\2\u020b\u024c\7%\2\2\u020c\u020d")
        buf.write("\7I\2\2\u020d\u024c\7%\2\2\u020e\u020f\7C\2\2\u020f\u024c")
        buf.write("\7%\2\2\u0210\u0211\7D\2\2\u0211\u024c\7%\2\2\u0212\u0213")
        buf.write("\7e\2\2\u0213\u024c\7%\2\2\u0214\u0215\7f\2\2\u0215\u024c")
        buf.write("\7%\2\2\u0216\u0217\7g\2\2\u0217\u024c\7%\2\2\u0218\u0219")
        buf.write("\7h\2\2\u0219\u024c\7%\2\2\u021a\u021b\7i\2\2\u021b\u024c")
        buf.write("\7%\2\2\u021c\u021d\7c\2\2\u021d\u024c\7%\2\2\u021e\u021f")
        buf.write("\7d\2\2\u021f\u024c\7%\2\2\u0220\u0221\7E\2\2\u0221\u0222")
        buf.write("\7%\2\2\u0222\u024c\7%\2\2\u0223\u0224\7F\2\2\u0224\u0225")
        buf.write("\7%\2\2\u0225\u024c\7%\2\2\u0226\u0227\7G\2\2\u0227\u0228")
        buf.write("\7%\2\2\u0228\u024c\7%\2\2\u0229\u022a\7H\2\2\u022a\u022b")
        buf.write("\7%\2\2\u022b\u024c\7%\2\2\u022c\u022d\7I\2\2\u022d\u022e")
        buf.write("\7%\2\2\u022e\u024c\7%\2\2\u022f\u0230\7C\2\2\u0230\u0231")
        buf.write("\7%\2\2\u0231\u024c\7%\2\2\u0232\u0233\7D\2\2\u0233\u0234")
        buf.write("\7%\2\2\u0234\u024c\7%\2\2\u0235\u0236\7e\2\2\u0236\u0237")
        buf.write("\7%\2\2\u0237\u024c\7%\2\2\u0238\u0239\7f\2\2\u0239\u023a")
        buf.write("\7%\2\2\u023a\u024c\7%\2\2\u023b\u023c\7g\2\2\u023c\u023d")
        buf.write("\7%\2\2\u023d\u024c\7%\2\2\u023e\u023f\7h\2\2\u023f\u0240")
        buf.write("\7%\2\2\u0240\u024c\7%\2\2\u0241\u0242\7i\2\2\u0242\u0243")
        buf.write("\7%\2\2\u0243\u024c\7%\2\2\u0244\u0245\7c\2\2\u0245\u0246")
        buf.write("\7%\2\2\u0246\u024c\7%\2\2\u0247\u0248\7d\2\2\u0248\u0249")
        buf.write("\7%\2\2\u0249\u024c\7%\2\2\u024a\u024c\t\b\2\2\u024b\u01bd")
        buf.write("\3\2\2\2\u024b\u01be\3\2\2\2\u024b\u01c0\3\2\2\2\u024b")
        buf.write("\u01c2\3\2\2\2\u024b\u01c4\3\2\2\2\u024b\u01c6\3\2\2\2")
        buf.write("\u024b\u01c8\3\2\2\2\u024b\u01ca\3\2\2\2\u024b\u01cc\3")
        buf.write("\2\2\2\u024b\u01ce\3\2\2\2\u024b\u01d0\3\2\2\2\u024b\u01d2")
        buf.write("\3\2\2\2\u024b\u01d4\3\2\2\2\u024b\u01d6\3\2\2\2\u024b")
        buf.write("\u01d8\3\2\2\2\u024b\u01da\3\2\2\2\u024b\u01dd\3\2\2\2")
        buf.write("\u024b\u01e0\3\2\2\2\u024b\u01e3\3\2\2\2\u024b\u01e6\3")
        buf.write("\2\2\2\u024b\u01e9\3\2\2\2\u024b\u01ec\3\2\2\2\u024b\u01ef")
        buf.write("\3\2\2\2\u024b\u01f2\3\2\2\2\u024b\u01f5\3\2\2\2\u024b")
        buf.write("\u01f8\3\2\2\2\u024b\u01fb\3\2\2\2\u024b\u01fe\3\2\2\2")
        buf.write("\u024b\u0201\3\2\2\2\u024b\u0204\3\2\2\2\u024b\u0206\3")
        buf.write("\2\2\2\u024b\u0208\3\2\2\2\u024b\u020a\3\2\2\2\u024b\u020c")
        buf.write("\3\2\2\2\u024b\u020e\3\2\2\2\u024b\u0210\3\2\2\2\u024b")
        buf.write("\u0212\3\2\2\2\u024b\u0214\3\2\2\2\u024b\u0216\3\2\2\2")
        buf.write("\u024b\u0218\3\2\2\2\u024b\u021a\3\2\2\2\u024b\u021c\3")
        buf.write("\2\2\2\u024b\u021e\3\2\2\2\u024b\u0220\3\2\2\2\u024b\u0223")
        buf.write("\3\2\2\2\u024b\u0226\3\2\2\2\u024b\u0229\3\2\2\2\u024b")
        buf.write("\u022c\3\2\2\2\u024b\u022f\3\2\2\2\u024b\u0232\3\2\2\2")
        buf.write("\u024b\u0235\3\2\2\2\u024b\u0238\3\2\2\2\u024b\u023b\3")
        buf.write("\2\2\2\u024b\u023e\3\2\2\2\u024b\u0241\3\2\2\2\u024b\u0244")
        buf.write("\3\2\2\2\u024b\u0247\3\2\2\2\u024b\u024a\3\2\2\2\u024c")
        buf.write("\62\3\2\2\2\r\2LUbfh\u0179\u017d\u0199\u01bb\u024b\3\b")
        buf.write("\2\2")
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
    T__8 = 9
    DOT = 10
    TIE = 11
    INT = 12
    LINEBEGIN = 13
    LINEEND = 14
    WS = 15
    COMMON_DURATION_CHORD_NUMERAL_LETTERS = 16
    DURATIONLETTER = 17
    ALTERATION = 18
    MODALITY = 19
    CHORDNUMERAL = 20
    CHORDMODALITY = 21
    NOTELETTERS = 22

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'['", "']'", "'('", "','", "')'", "':'", "'/'", "'<'", "'>'", 
            "'@'", "'-'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>",
            "DOT", "TIE", "INT", "LINEBEGIN", "LINEEND", "WS", "COMMON_DURATION_CHORD_NUMERAL_LETTERS", 
            "DURATIONLETTER", "ALTERATION", "MODALITY", "CHORDNUMERAL", 
            "CHORDMODALITY", "NOTELETTERS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "DOT", "TIE", "INT", "LINEBEGIN", "LINEEND", 
                  "WS", "COMMON_DURATION_CHORD_NUMERAL_LETTERS", "DURATIONLETTER", 
                  "ALTERATION", "USER_MODALITY", "SYSTEM_MODALITIES", "MODALITY", 
                  "CHORDNUMERAL", "CHORDMODALITY", "NOTELETTERS" ]

    grammarFileName = "LineGrammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


        self.lc = LineConstructor();
        self._notelist = list()


