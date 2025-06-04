# LangSec-SysML-Prototype

This repository demonstrates the feasibility of using **SysML models** in Cameo to define message grammars, and automatically generate **secure parsers** using **ANTLR**. It follows the LANGSEC principle of making input structure explicit, verifiable, and machine-readable.
---

## 🧭 Objective

Show that a system model in SysML can:

- Define message structure using stereotypes and tags
- Be programmatically extracted using Jython (Cameo’s OpenAPI)
- Generate a `.g4` grammar for ANTLR
- Produce a working parser that accepts **only valid input**
- Be run without installing extra tools beyond Cameo, Java, and Python


## 🧱 Step 1: Build the SysML Model in Cameo

### 1.1 Create a New Project

- Open Cameo
- File → New Project → Name it something like `ParserModelDemo`

### 1.2 Create a Block Named `HeartbeatMessage`

1. In the **Containment Tree**, right-click on the top-level `Model`  
2. Select: `Create Element → Block`  
3. Name the block: `HeartbeatMessage`

### 1.3 Add Value Properties

Each **Value Property** defines a field in the message structure. You will add:

| Name      | Type    | Purpose                          |
|-----------|---------|----------------------------------|
| `counter` | Integer | A message sequence or counter ID |
| `status`  | Integer | Status field (0 or 1 expected)   |
| `checksum`| Integer | Final checksum or CRC byte       |

#### How to Add:

1. Double-click `HeartbeatMessage` to open its **Specification**
2. Scroll to or search for **Owned Attributes**
3. Click the `+` and choose **Value Property**
4. Set the **name** (e.g., `counter`)
5. Click the `Type` field → click `...` → choose `Integer`
6. Repeat for `status` and `checksum`

You now have a block that structurally defines a 3-field message.

---

## 🧩 Step 2: Create and Apply a Custom Stereotype

### 2.1 Create a Profile

1. In the Containment Tree, right-click a **Package** (not the root `Model`)
2. Select `Create Element → Profile`
3. Name it: `ParserProfile`

### 2.2 Add the `GrammarRule` Stereotype

1. Right-click `ParserProfile` → `Create Element → Stereotype`
2. Name it: `GrammarRule`
3. Open the Stereotype’s Specification → Add a **Tag Definition**:
   - Name: `ruleText`
   - Type: `String`

### 2.3 Apply the Profile to the Model

1. Right-click the top-level `Model`
2. Select `Specification`
3. Find the field **Applied Profiles**
4. Click `+` and select `ParserProfile`

### 2.4 Annotate Properties with Grammar

1. Open the `Specification` of each property (`counter`, etc.)
2. In **Applied Stereotypes**, add `GrammarRule`
3. In **Tags**, set:
   - `ruleText = INT`

You now have a model that not only defines structure, but **declares grammar semantics**.

---

## 🐍 Step 3: Extract Grammar Using Jython in Cameo

### 3.1 Open the Jython Console

- Tools → Scripting Engine → Select Language: `Jython`

### 3.2 Run the Script

Paste this into the console:

```python
from com.nomagic.magicdraw.core import Application
from com.nomagic.uml2.ext.jmi.helpers import StereotypesHelper
from com.nomagic.uml2.ext.magicdraw.classes.mdkernel import Class, Property, Package

project = Application.getInstance().getProject()
log = Application.getInstance().getGUILog()
model = project.getModel()

def find_block(name):
    for element in model.getOwnedElement():
        if isinstance(element, Class) and element.getName() == name:
            return element
    return None

def find_stereotype():
    for element in model.getOwnedElement():
        if isinstance(element, Package) and element.getName() == "ModelingCore":
            for subelement in element.getOwnedElement():
                try:
                    if subelement.getName() == "ParserProfile":
                        for s in subelement.getOwnedElement():
                            if s.getName() == "GrammarRule":
                                return s
                except:
                    continue
    return None

block = find_block("HeartbeatMessage")
stereotype = find_stereotype()

if block and stereotype:
    log.log("grammar Heartbeat;\n")
    log.log("heartbeat: " + " ".join([p.getName() for p in block.getOwnedAttribute()]) + " EOF;\n")
    for attr in block.getOwnedAttribute():
        if isinstance(attr, Property):
            if StereotypesHelper.hasStereotype(attr, stereotype):
                val = StereotypesHelper.getStereotypePropertyValue(attr, stereotype, "ruleText")
                log.log("%s: %s;" % (attr.getName(), val[0] if val else "<empty>"))
    log.log("\nINT: [0-9]+;")
    log.log("WS: [ \\t\\r\\n]+ -> skip;")
