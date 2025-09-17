import sys
import json
from antlr4 import *
from J1939_TP_CMLexer import J1939_TP_CMLexer
from J1939_TP_CMParser import J1939_TP_CMParser

# --- Recursive tree to JSON converter ---
def tree_to_dict(ctx, rule_names):
    """
    Recursively convert an ANTLR parse tree into a nested Python dict.
    """
    if ctx.getChildCount() == 0:
        # Leaf node: return token text
        return ctx.getText()

    rule_name = rule_names[ctx.getRuleIndex()]
    children = {}

    for i in range(ctx.getChildCount()):
        child = ctx.getChild(i)
        if isinstance(child, TerminalNode):
            # Terminal tokens just as plain text
            text = child.getText()
            if text not in ["<EOF>", "\n", "\r", "\t", " "]:
                children.setdefault("tokens", []).append(text)
        else:
            # Parser rule node
            child_name = rule_names[child.getRuleIndex()]
            value = tree_to_dict(child, rule_names)

            # If same rule appears multiple times, collect as list
            if child_name in children:
                if not isinstance(children[child_name], list):
                    children[child_name] = [children[child_name]]
                children[child_name].append(value)
            else:
                children[child_name] = value

    return {rule_name: children} if rule_name != "tp_cm_rts" else children

# --- Main function ---
def parse_hex_to_json(hex_string):
    # Clean spaces/newlines
    hex_string = hex_string.replace(" ", "").replace("\n", "")

    # Run lexer and parser
    input_stream = InputStream(hex_string)
    lexer = J1939_TP_CMLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = J1939_TP_CMParser(tokens)

    # Parse using the main rule
    tree = parser.tp_cm_rts()

    # Convert to JSON
    rule_names = parser.ruleNames
    return tree_to_dict(tree, rule_names)

# --- Entry point ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        hex_input = sys.argv[1]
    else:
        hex_input = "10 2A 00 06 FF 00 12 34"

    print("DEBUG: Raw input string ->", repr(hex_input))

    json_result = parse_hex_to_json(hex_input)
    print(json.dumps(json_result, indent=2))
