# Generated from SqlCurrent.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,9,60,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,2,1,
        2,1,3,1,3,1,4,1,4,1,5,4,5,36,8,5,11,5,12,5,37,1,5,1,5,1,6,4,6,43,
        8,6,11,6,12,6,44,1,7,4,7,48,8,7,11,7,12,7,49,1,8,1,8,5,8,54,8,8,
        10,8,12,8,57,9,8,1,8,1,8,0,0,9,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,
        8,17,9,1,0,4,3,0,9,10,13,13,32,32,1,0,48,57,4,0,48,57,65,90,95,95,
        97,122,5,0,46,46,48,58,65,90,95,95,97,122,63,0,1,1,0,0,0,0,3,1,0,
        0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,
        0,0,15,1,0,0,0,0,17,1,0,0,0,1,19,1,0,0,0,3,26,1,0,0,0,5,28,1,0,0,
        0,7,30,1,0,0,0,9,32,1,0,0,0,11,35,1,0,0,0,13,42,1,0,0,0,15,47,1,
        0,0,0,17,51,1,0,0,0,19,20,5,115,0,0,20,21,5,101,0,0,21,22,5,114,
        0,0,22,23,5,118,0,0,23,24,5,101,0,0,24,25,5,114,0,0,25,2,1,0,0,0,
        26,27,5,123,0,0,27,4,1,0,0,0,28,29,5,125,0,0,29,6,1,0,0,0,30,31,
        5,59,0,0,31,8,1,0,0,0,32,33,5,58,0,0,33,10,1,0,0,0,34,36,7,0,0,0,
        35,34,1,0,0,0,36,37,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,39,1,
        0,0,0,39,40,6,5,0,0,40,12,1,0,0,0,41,43,7,1,0,0,42,41,1,0,0,0,43,
        44,1,0,0,0,44,42,1,0,0,0,44,45,1,0,0,0,45,14,1,0,0,0,46,48,7,2,0,
        0,47,46,1,0,0,0,48,49,1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,50,16,
        1,0,0,0,51,55,5,39,0,0,52,54,7,3,0,0,53,52,1,0,0,0,54,57,1,0,0,0,
        55,53,1,0,0,0,55,56,1,0,0,0,56,58,1,0,0,0,57,55,1,0,0,0,58,59,5,
        39,0,0,59,18,1,0,0,0,6,0,37,44,49,53,55,1,6,0,0
    ]

class SqlCurrentLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    WS = 6
    INT_LITERAL = 7
    SYMBOL_ID = 8
    STRING_LITERAL = 9

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'server'", "'{'", "'}'", "';'", "':'" ]

    symbolicNames = [ "<INVALID>",
            "WS", "INT_LITERAL", "SYMBOL_ID", "STRING_LITERAL" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "WS", "INT_LITERAL", 
                  "SYMBOL_ID", "STRING_LITERAL" ]

    grammarFileName = "SqlCurrent.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


