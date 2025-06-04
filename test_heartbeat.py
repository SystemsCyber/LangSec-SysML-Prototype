from antlr4 import *
from HeartbeatLexer import HeartbeatLexer
from HeartbeatParser import HeartbeatParser
from antlr4.error.ErrorListener import ErrorListener

class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("Syntax error at line %d:%d - %s" % (line, column, msg))

input_stream = InputStream("123 1 999")
# check erronous input streams.....
# input_stream = InputStream("123 X 999")
# input_stream = InputStream("123 1 999 22")
lexer = HeartbeatLexer(input_stream)
lexer.removeErrorListeners()
lexer.addErrorListener(ThrowingErrorListener())

token_stream = CommonTokenStream(lexer)
parser = HeartbeatParser(token_stream)
parser.removeErrorListeners()
parser.addErrorListener(ThrowingErrorListener())

try:
    tree = parser.heartbeat()
    print("✅ Parsed successfully!")
    print(tree.toStringTree(recog=parser))
except Exception as e:
    print("❌ Parse failed:", e)
