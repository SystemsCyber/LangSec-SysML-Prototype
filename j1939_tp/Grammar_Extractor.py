# ========================================================================
# SysML to ANTLR Grammar Extractor (Modular Field Rules)
#
# - Scans SysML model for <<GrammarRule>> blocks
# - Reads <<Field>> properties and their 'start' tag
# - If a field has <<Enum>> stereotype, resolves its fixed value
# - Generates modular ANTLR grammar with:
#     * top-level rule (e.g., tp_cm_rts)
#     * separate parser rules for each field
#     * standard terminal definitions
# ========================================================================

from com.nomagic.magicdraw.core import Application
from com.nomagic.uml2.ext.magicdraw.classes.mdkernel import Class, Property, Package
from com.nomagic.uml2.ext.jmi.helpers import StereotypesHelper

# -------------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------------
project = Application.getInstance().getProject()
log = Application.getInstance().getGUILog()
model = project.getModel()

# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------
def find_package_recursive(element, target_name):
    """Find a package by name recursively."""
    if isinstance(element, Package) and element.getName() == target_name:
        return element
    for child in element.getOwnedElement():
        found = find_package_recursive(child, target_name)
        if found:
            return found
    return None

def get_field_length(prop):
    """Determine byte length based on type name."""
    if prop.getType() is None:
        return 1
    tname = prop.getType().getName().lower()
    if tname == "uint16":
        return 2
    elif tname == "uint24":
        return 3
    return 1  # Default = 1 byte

def get_enum_control_value(prop):
    """
    Reads <<Enum>> stereotype and returns the selected value.
    Returns (tag, value) or None if not present.
    """
    enum_props = ["rts", "cts", "bam", "eom", "abort"]
    for tag in enum_props:
        try:
            vals = StereotypesHelper.getStereotypePropertyValue(prop, "Enum", tag)
            if vals and len(vals) > 0:
                return (tag, str(vals[0]).strip())
        except:
            continue
    return None

# -------------------------------------------------------------------------
# Main Grammar Generator
# -------------------------------------------------------------------------
def generate_grammar():
    lines = []
    lines.append("// Auto-generated from SysML J1939 TP model")
    lines.append("grammar J1939_TP_CM;")
    lines.append("")

    blocks_pkg = find_package_recursive(model, "Blocks")
    if blocks_pkg is None:
        log.log("ERROR: No 'Blocks' package found in model.")
        return

    log.log("Found 'Blocks' package: {}".format(blocks_pkg.getName()))

    # Process each block
    for block in blocks_pkg.getOwnedElement():
        if not isinstance(block, Class):
            continue
        if not StereotypesHelper.hasStereotypeOrDerived(block, "GrammarRule"):
            continue

        log.log("Processing block: {}".format(block.getName()))
        block_rule_name = block.getName().lower()
        field_info = []

        # Collect fields
        for prop in block.getOwnedAttribute():
            if not isinstance(prop, Property):
                continue
            if not StereotypesHelper.hasStereotypeOrDerived(prop, "Field"):
                continue

            # Start tag
            start_vals = StereotypesHelper.getStereotypePropertyValue(prop, "Field", "start")
            if not start_vals or len(start_vals) == 0:
                log.log("WARNING: Field '{}' missing start tag, skipping.".format(prop.getName()))
                continue
            try:
                start = int(str(start_vals[0]))
            except:
                log.log("ERROR: Invalid start value '{}' for field '{}'.".format(start_vals, prop.getName()))
                continue

            # Enum?
            control_info = get_enum_control_value(prop)
            if control_info:
                tag_name, control_val = control_info
                fixed_hex = format(int(control_val), '02X')
                field_info.append({
                    "ruleName": prop.getName(),
                    "start": start,
                    "length": 1,
                    "fixedHex": fixed_hex,
                    "comment": "{} ({})".format(prop.getName(), tag_name)
                })
            else:
                length = get_field_length(prop)
                field_info.append({
                    "ruleName": prop.getName(),
                    "start": start,
                    "length": length,
                    "fixedHex": None,
                    "comment": prop.getName()
                })

        # Sort by byte position
        field_info.sort(key=lambda x: x["start"])
        if len(field_info) == 0:
            log.log("WARNING: No fields in block {}".format(block.getName()))
            continue

        # -----------------------------------------------------------------
        # Emit top-level rule
        # -----------------------------------------------------------------
        lines.append("// Rule for {}".format(block.getName()))
        for f in field_info:
            if f["length"] == 1:
                lines.append("// Byte {} : {}".format(f["start"], f["comment"]))
            else:
                end = f["start"] + f["length"] - 1
                lines.append("// Byte {}-{} : {}".format(f["start"], end, f["comment"]))

        rule_body = " ".join([f["ruleName"] for f in field_info]) + " EOF"
        lines.append("{} : {} ;\n".format(block_rule_name, rule_body))

        # -----------------------------------------------------------------
        # Emit field-specific rules
        # -----------------------------------------------------------------
        for f in field_info:
            if f["fixedHex"]:
                lines.append("{} : '{}' ; // {}\n".format(f["ruleName"], f["fixedHex"], f["comment"]))
            elif f["length"] == 1:
                lines.append("{} : UINT8 ; // {}\n".format(f["ruleName"], f["comment"]))
            else:
                lines.append("{} : {} ; // {}\n".format(
                    f["ruleName"],
                    " ".join(["UINT8"] * f["length"]),
                    f["comment"]
                ))

    # ---------------------------------------------------------------------
    # Terminal rules
    # ---------------------------------------------------------------------
    lines.append("// Terminal rules for J1939 data types")
    lines.append("UINT8  : [0-9A-F] [0-9A-F] ;")
    lines.append("WS     : [ \\t\\r\\n]+ -> skip ;")
    lines.append("")

    # ---------------------------------------------------------------------
    # Print grammar
    # ---------------------------------------------------------------------
    log.log("\n==== GENERATED ANTLR GRAMMAR ====\n")
    for line in lines:
        log.log(line)
    log.log("==== END GRAMMAR ====\n")

# -------------------------------------------------------------------------
# Run
# -------------------------------------------------------------------------
generate_grammar()
