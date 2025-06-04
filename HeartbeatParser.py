# Generated from Heartbeat.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,2,20,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,0,1,0,1,0,1,1,
        1,1,1,2,1,2,1,3,1,3,1,3,0,0,4,0,2,4,6,0,0,15,0,8,1,0,0,0,2,13,1,
        0,0,0,4,15,1,0,0,0,6,17,1,0,0,0,8,9,3,2,1,0,9,10,3,4,2,0,10,11,3,
        6,3,0,11,12,5,0,0,1,12,1,1,0,0,0,13,14,5,1,0,0,14,3,1,0,0,0,15,16,
        5,1,0,0,16,5,1,0,0,0,17,18,5,1,0,0,18,7,1,0,0,0,0
    ]

class HeartbeatParser ( Parser ):

    grammarFileName = "Heartbeat.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "INT", "WS" ]

    RULE_heartbeat = 0
    RULE_counter = 1
    RULE_status = 2
    RULE_checksum = 3

    ruleNames =  [ "heartbeat", "counter", "status", "checksum" ]

    EOF = Token.EOF
    INT=1
    WS=2

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class HeartbeatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def counter(self):
            return self.getTypedRuleContext(HeartbeatParser.CounterContext,0)


        def status(self):
            return self.getTypedRuleContext(HeartbeatParser.StatusContext,0)


        def checksum(self):
            return self.getTypedRuleContext(HeartbeatParser.ChecksumContext,0)


        def EOF(self):
            return self.getToken(HeartbeatParser.EOF, 0)

        def getRuleIndex(self):
            return HeartbeatParser.RULE_heartbeat

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHeartbeat" ):
                listener.enterHeartbeat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHeartbeat" ):
                listener.exitHeartbeat(self)




    def heartbeat(self):

        localctx = HeartbeatParser.HeartbeatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_heartbeat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.counter()
            self.state = 9
            self.status()
            self.state = 10
            self.checksum()
            self.state = 11
            self.match(HeartbeatParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CounterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(HeartbeatParser.INT, 0)

        def getRuleIndex(self):
            return HeartbeatParser.RULE_counter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCounter" ):
                listener.enterCounter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCounter" ):
                listener.exitCounter(self)




    def counter(self):

        localctx = HeartbeatParser.CounterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_counter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self.match(HeartbeatParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatusContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(HeartbeatParser.INT, 0)

        def getRuleIndex(self):
            return HeartbeatParser.RULE_status

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatus" ):
                listener.enterStatus(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatus" ):
                listener.exitStatus(self)




    def status(self):

        localctx = HeartbeatParser.StatusContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_status)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self.match(HeartbeatParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ChecksumContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(HeartbeatParser.INT, 0)

        def getRuleIndex(self):
            return HeartbeatParser.RULE_checksum

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChecksum" ):
                listener.enterChecksum(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChecksum" ):
                listener.exitChecksum(self)




    def checksum(self):

        localctx = HeartbeatParser.ChecksumContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_checksum)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.match(HeartbeatParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





