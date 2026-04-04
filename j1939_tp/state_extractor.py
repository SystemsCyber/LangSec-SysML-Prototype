# ============================================================
# SysML StateMachine → SCXML (LOG DEMO, GUI-SAFE)
# ============================================================

from com.nomagic.magicdraw.core import Application
from com.nomagic.uml2.ext.magicdraw.statemachines.mdbehaviorstatemachines import StateMachine
from com.nomagic.uml2.ext.magicdraw.commonbehaviors.mdcommunications import CallEvent
from com.nomagic.uml2.ext.magicdraw.classes.mdkernel import Package

app = Application.getInstance()
project = app.getProject()
model = project.getModel()
log = app.getGUILog()

# ------------------------------------------------------------
# Helper: safe logging (NO < > EVER)
# ------------------------------------------------------------
def log_scxml(line):
    line = line.replace("<", "[")
    line = line.replace(">", "]")
    log.log(line)

# ------------------------------------------------------------
# Model lookup helpers
# ------------------------------------------------------------
def find_package(root, name):
    if isinstance(root, Package) and root.getName() == name:
        return root
    for el in root.getOwnedElement():
        p = find_package(el, name)
        if p:
            return p
    return None

def find_sm(root, name):
    for el in root.getOwnedElement():
        if isinstance(el, StateMachine) and el.getName() == name:
            return el
        sm = find_sm(el, name)
        if sm:
            return sm
    return None

# ------------------------------------------------------------
# Locate model
# ------------------------------------------------------------
pkg = find_package(model, "StateMachine")
if pkg is None:
    raise Exception("Package not found")

sm = find_sm(pkg, "TP_Sender")
if sm is None:
    raise Exception("StateMachine not found")

region = sm.getRegion()[0]

# ------------------------------------------------------------
# DEMO OUTPUT
# ------------------------------------------------------------
log.log("===== SCXML DEMO OUTPUT =====")

log_scxml("<scxml initial=\"Idle\">")

for t in region.getTransition():
    src = t.getSource()
    tgt = t.getTarget()

    if not src or not tgt:
        continue
    if not src.getName() or not tgt.getName():
        continue

    line = "<transition source=\"%s\" target=\"%s\"" % (
        src.getName(), tgt.getName()
    )

    # Trigger
    triggers = t.getTrigger()
    if triggers and len(triggers) > 0:
        trig = triggers[0]
        event = trig.getEvent()
        if isinstance(event, CallEvent):
            op = event.getOperation()
            if op:
                line += " event=\"%s\"" % op.getName()

    # Guard
    guard = t.getGuard()
    if guard:
        spec = guard.getSpecification()
        if spec and hasattr(spec, "getBody"):
            body = spec.getBody()
            if body and len(body) > 0:
                cond = body[0].replace("\n", " ").replace('"', "'")
                line += " cond=\"%s\"" % cond

    line += " />"
    log_scxml(line)

log_scxml("</scxml>")

log.log("===== END SCXML =====")