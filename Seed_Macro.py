from com.nomagic.magicdraw.core import Application
from com.nomagic.uml2.ext.jmi.helpers import StereotypesHelper
from com.nomagic.uml2.ext.magicdraw.classes.mdkernel import Class, Property, Package

project = Application.getInstance().getProject()
log = Application.getInstance().getGUILog()
model = project.getModel()

def find_block_top_level(name):
    for element in model.getOwnedElement():
        if isinstance(element, Class) and element.getName() == name:
            return element
    return None

def find_grammar_rule_stereotype():
    for element in model.getOwnedElement():
        if isinstance(element, Package) and element.getName() == "ModelingCore":
            for subelement in element.getOwnedElement():
                try:
                    if subelement.getName() == "ParserProfile":
                        for s in subelement.getOwnedElement():
                            try:
                                if s.getName() == "GrammarRule":
                                    return s
                            except:
                                continue
                except:
                    continue
    return None

block = find_block_top_level("Heartbeat")
stereotype = find_grammar_rule_stereotype()

if block is None or stereotype is None:
    log.log("ERROR: Block or stereotype not found.")
else:
    # Begin grammar
    log.log("\n--- BEGIN ANTLR GRAMMAR ---")
    log.log("grammar Heartbeat;\n")

    # Message rule
    log.log("heartbeat: " + " ".join([p.getName() for p in block.getOwnedAttribute()]) + ";\n")

    # Fields
    for attr in block.getOwnedAttribute():
        if isinstance(attr, Property):
            if StereotypesHelper.hasStereotype(attr, stereotype):
                tag_val = StereotypesHelper.getStereotypePropertyValue(attr, stereotype, "ruleText")
                rule_text = tag_val[0] if tag_val and len(tag_val) > 0 else "<empty>"
                log.log("%s: %s;" % (attr.getName(), rule_text))

    # Common tokens
    log.log("\nINT: [0-9]+;")
    log.log("WS: [ \\t\\r\\n]+ -> skip;")
    log.log("--- END ANTLR GRAMMAR ---\n")
