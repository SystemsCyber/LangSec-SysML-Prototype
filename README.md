# LangSec-SysML-Prototype

This repository provides a rudimentary proof of concept (PoC) of the feasibility of using SysML models in Cameo to define message grammars and automatically generate secure parsers using ANTLR. It follows the LANGSEC principle of making input structure explicit, verifiable, and machine-readable. Further testing for a ROS1 project is also being integrated. The current ROS deployment includes ROS integration on a BeagleBone Black, enabling integration with J1939/CAN networks as a basic parser for command and request messages.

## SysML Description

This project uses a minimal SysML block model to represent a simple, structured software message called **Heartbeat**. The model defines a message with three fields:
 - counter
 - status
 - checksum
Each of these fields is modeled as a value property inside a Block in Cameo. The objective is to annotate these properties with formal grammar rules, extract them programmatically, and generate a parser that can enforce message correctness based on the model. The purpose of this PoC is to show that interface contracts modeled in SysML can be used to drive secure input validation instead of writing ad hoc parsers by hand.

<!--

The repository contains:
- The SysML Model: A Cameo `.mdzip` file defining a HeartbeatMessage block. Each property is annotated with a custom <<GrammarRule>> stereotype containing a ruleText tag.
- Jython script: A script runnable inside Cameo’s Jython console that traverses the model, extracts each field’s name and grammar rule, and prints a complete ANTLR `.g4` grammar definition to the Messages pane.
- ANTLR grammar: A `.g4` grammar file generated from the model.
- ANTLR-Generated Parser Files
- Test Script

## Objective

This PoC shows that:

- Define message structure using stereotypes and tags
- Be programmatically extracted using Jython (Cameo’s OpenAPI)
- Generate a `.g4` grammar for ANTLR
- Produce a working parser that accepts **only valid input**

## Getting Started:

If you want to test the parser only, skip directly to Step 5.
If you want to build from scratch, follow all steps below.

## Step 1: Build the SysML Model in Cameo

### 1.1 Create a New Project

- Open Cameo
- File → New Project → Name it

### 1.2 Create a Block Named `Heartbeat`

1. In the **Containment Tree**, right-click on the top-level `Model`  
2. Select: `Create Element → Block`  
3. Name the block: `Heartbeat`

### 1.3 Add Value Properties

Each **Value Property** defines a field in the message structure. You will add:

| Name      | Type    | Purpose                          |
|-----------|---------|----------------------------------|
| `counter` | Integer | A message sequence or counter ID |
| `status`  | Integer | Status field                     |
| `checksum`| Integer | Final checksum or CRC byte       |

#### How to Add:

1. Double-click `HeartbeatMessage` to open its **Specification**
2. Scroll to or search for **Owned Attributes**
3. Click the `+` and choose **Value Property**
4. Set the **name** (e.g., `counter`)
5. Click the `Type` field → click `...` → choose `Integer`
6. Repeat for `status` and `checksum`

You now have a block that structurally defines a 3-field message.


## Step 2: Create and Apply a Custom Stereotype

### 2.1 Create a Profile

1. In the Containment Tree, create a **Package**, right-click the **Package**
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


## Step 3: Extract Grammar Using Jython in Cameo

### 3.1 Open the Jython Console

- Tools → Scripting Engine → Select Language: `Jython`

### 3.2 Run the Script

Paste the code in `Seed_Macro` into the console. Run it. It will provide an output of the `.g4` file. Save the output as Heartbeat.g4

## Step 4: Generate a Parser with ANTLR

### 4.1 Install Prerequisites

- Java
- Python
- ANTLR runtime:
```
  pip install antlr4-python3-runtime
```
Download antlr from: ```https://www.antlr.org/download.html```
Save to same directory as your project and rename `antlr.jar`

### 4.2 Generate Parser Code

```
java -jar antlr.jar -Dlanguage=Python3 Heartbeat.g4
```

## Step 5 Test Parser
```
python test_heartbeat.py
```

Change: ```input_stream = InputStream("123 1 999")``` to ```input_stream = InputStream("123 X 999")``` or ```input_stream = InputStream("123 1 999 22")``` to test out invalid inputs -->
