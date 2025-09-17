# Generated from J1939_TP_CM.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,3,20,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,0,1,1,1,1,1,1,1,
        2,4,2,15,8,2,11,2,12,2,16,1,2,1,2,0,0,3,1,1,3,2,5,3,1,0,2,2,0,48,
        57,65,70,3,0,9,10,13,13,32,32,20,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,
        0,0,1,7,1,0,0,0,3,10,1,0,0,0,5,14,1,0,0,0,7,8,5,49,0,0,8,9,5,48,
        0,0,9,2,1,0,0,0,10,11,7,0,0,0,11,12,7,0,0,0,12,4,1,0,0,0,13,15,7,
        1,0,0,14,13,1,0,0,0,15,16,1,0,0,0,16,14,1,0,0,0,16,17,1,0,0,0,17,
        18,1,0,0,0,18,19,6,2,0,0,19,6,1,0,0,0,2,0,16,1,6,0,0
    ]

class J1939_TP_CMLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    UINT8 = 2
    WS = 3

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'10'" ]

    symbolicNames = [ "<INVALID>",
            "UINT8", "WS" ]

    ruleNames = [ "T__0", "UINT8", "WS" ]

    grammarFileName = "J1939_TP_CM.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


