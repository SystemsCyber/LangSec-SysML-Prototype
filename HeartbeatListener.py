# Generated from Heartbeat.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .HeartbeatParser import HeartbeatParser
else:
    from HeartbeatParser import HeartbeatParser

# This class defines a complete listener for a parse tree produced by HeartbeatParser.
class HeartbeatListener(ParseTreeListener):

    # Enter a parse tree produced by HeartbeatParser#heartbeat.
    def enterHeartbeat(self, ctx:HeartbeatParser.HeartbeatContext):
        pass

    # Exit a parse tree produced by HeartbeatParser#heartbeat.
    def exitHeartbeat(self, ctx:HeartbeatParser.HeartbeatContext):
        pass


    # Enter a parse tree produced by HeartbeatParser#counter.
    def enterCounter(self, ctx:HeartbeatParser.CounterContext):
        pass

    # Exit a parse tree produced by HeartbeatParser#counter.
    def exitCounter(self, ctx:HeartbeatParser.CounterContext):
        pass


    # Enter a parse tree produced by HeartbeatParser#status.
    def enterStatus(self, ctx:HeartbeatParser.StatusContext):
        pass

    # Exit a parse tree produced by HeartbeatParser#status.
    def exitStatus(self, ctx:HeartbeatParser.StatusContext):
        pass


    # Enter a parse tree produced by HeartbeatParser#checksum.
    def enterChecksum(self, ctx:HeartbeatParser.ChecksumContext):
        pass

    # Exit a parse tree produced by HeartbeatParser#checksum.
    def exitChecksum(self, ctx:HeartbeatParser.ChecksumContext):
        pass



del HeartbeatParser