# LangSec-SysML-Prototype

This repository provides a rudimentary proof of concept (PoC) of the feasibility of using SysML models in Cameo to define message grammars and automatically generate secure parsers using ANTLR. It follows the LANGSEC principle of making input structure explicit, verifiable, and machine-readable. 

## SysML Description

This project uses a minimal SysML block model to represent a SAE J1939 Transport Protocol message called **TP_RTS**. 
Each field of the message is modeled as a value property inside a Block in Cameo. The objective is to annotate these properties with formal grammar rules, extract them programmatically, and generate a parser that can enforce message correctness based on the model. The purpose of this PoC is to show that interface contracts modeled in SysML can be used to drive secure input validation instead of writing ad hoc parsers by hand.


## Step 1: Extract Grammar Using Jython in Cameo

### 1.1 Open the Jython Console

- Tools → Scripting Engine → Select Language: `Jython`

### 3.2 Run the Script

Paste the code in `Grammar_Extractor.py` into the console. Run it. It will provide an output of the `.g4` file. Save the output as J1939_TP_CM.g4

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
java -jar antlr.jar -Dlanguage=Python3 J1939_TP_CM.g4
```

## Step 5 Test Parser
```
python test_tp_cm_parser.py
```
