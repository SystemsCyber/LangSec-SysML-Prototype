import json
from antlr4 import *
from antlr4.error.ErrorStrategy import BailErrorStrategy
from antlr4.error.Errors import ParseCancellationException

from J1939_TP_CMLexer import J1939_TP_CMLexer
from J1939_TP_CMParser import J1939_TP_CMParser


# ------------------------------------------------------------
# Parse helper (STRICT)
# ------------------------------------------------------------
def parse_frame(hex_string, rule="rts"):
    input_stream = InputStream(hex_string)
    lexer = J1939_TP_CMLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = J1939_TP_CMParser(tokens)

    # Strict mode: no recovery
    parser.removeErrorListeners()
    parser._errHandler = BailErrorStrategy()

    try:
        if rule == "rts":
            tree = parser.tp_cm_rts()
        elif rule == "cts":
            tree = parser.tp_cm_cts()
        else:
            raise ValueError("Unknown rule")

        return tree, parser.ruleNames

    except ParseCancellationException:
        return None, None


# ------------------------------------------------------------
# Convert tree → JSON
# ------------------------------------------------------------
def tree_to_dict(ctx, rule_names):
    if ctx.getChildCount() == 0:
        return ctx.getText()

    children = {}

    for i in range(ctx.getChildCount()):
        child = ctx.getChild(i)

        if isinstance(child, TerminalNode):
            text = child.getText()
            if text not in ["<EOF>", " "]:
                children.setdefault("tokens", []).append(text)
        else:
            child_name = rule_names[child.getRuleIndex()]
            value = tree_to_dict(child, rule_names)
            children[child_name] = value

    return children


# ------------------------------------------------------------
# Test runner
# ------------------------------------------------------------
def run_test(name, hex_input, rule, expect_valid=True):
    print("\n==============================")
    print(f"TEST: {name}")
    print(f"INPUT: {hex_input}")
    print(f"RULE: {rule}")

    tree, rule_names = parse_frame(hex_input, rule)

    if tree is None:
        if expect_valid:
            print("❌ FAIL (expected valid, got INVALID)")
        else:
            print("✅ PASS (correctly rejected)")
        return

    if not expect_valid:
        print("❌ FAIL (expected rejection, but parsed)")
        return

    print("✅ PASS (valid frame)")

    # Print JSON
    result = tree_to_dict(tree, rule_names)
    print(json.dumps(result, indent=2))


# ------------------------------------------------------------
# Test cases
# ------------------------------------------------------------
if __name__ == "__main__":

    tests = [
        # -----------------------
        # VALID RTS
        # -----------------------
        ("Valid RTS", "10 2A 00 06 FF 00 12 34", "rts", True),

        # -----------------------
        # INVALID RTS (wrong control byte)
        # -----------------------
        ("Invalid RTS control byte", "13 2A 00 06 FF 00 12 34", "rts", False),

        # -----------------------
        # INVALID RTS (too short)
        # -----------------------
        ("Invalid RTS short frame", "10 2A 00 06 FF 00 12", "rts", False),

        # -----------------------
        # INVALID RTS (extra byte)
        # -----------------------
        ("Invalid RTS extra byte", "10 2A 00 06 FF 00 12 34 AA", "rts", False),

        # -----------------------
        # VALID CTS
        # -----------------------
        ("Valid CTS", "11 05 01 00 00 00 12 34", "cts", True),

        # -----------------------
        # INVALID CTS (wrong control byte)
        # -----------------------
        ("Invalid CTS control byte", "10 05 01 00 00 00 12 34", "cts", False),

        # -----------------------
        # INVALID CTS (bad length)
        # -----------------------
        ("Invalid CTS short", "11 05 01 00 00 00 12", "cts", False),
    ]

    for name, hex_input, rule, expected in tests:
        run_test(name, hex_input, rule, expected)