# Probabilistic Earley Parser

An efficient, modular Earley parser implemented in Python for parsing Probabilistic Context-Free Grammars (PCFG). The parser not only determines if a sentence is grammatically valid but also extracts the minimum-cost Viterbi paths and exhaustively generates all valid structural parse trees, outputting them in beautifully formatted S-expressions along with their calculated optimal base-2 log costs.

## Core Features
1. **Dynamic Programming Viterbi Extraction**: Retains $O(n^3)$ temporal and $O(n^2)$ spatial complexity while extracting strictly the mathematically optimal derivation path based on the highest probability (lowest cost).
2. **Exhaustive Ambiguity Tracking**: Decouples the state-tracking backpointers from the Viterbi bounds, allowing absolute combinatorial recovery of all ambiguous valid structures (like classic PP-attachment issues).
3. **Self-Contained & Modular**: Strictly relies on standard Python libraries. The logic is cleanly decoupled into grammar ingest routines, parsing agenda management, and input pipeline execution.

## Project Structure

```text
├── parse.py           # Main CLI entry point encapsulating arguments and pipeline execution
├── earley.py          # Core Earley parsing algorithm, state management, and S-expression formatter
├── grammar.py         # PCFG ingest module tracking statistical costs (-log2 conversions)
├── Report.md          # Theoretical assignment answers, structural logic, and Big-O efficiency analysis
├── time/
│   ├── time.gr        # Baseline PCFG model for "time flies" ambiguity 
│   └── time.sen       # Input sentences  
└── soldier/
    ├── soldier.gr     # Custom ambiguous PCFG structure for PP-attachment evaluation
    └── soldier.sen    # Input sentences
```

## Prerequisites
- **Python 3.6+** (Standard Native Library only; no `pip installs` or external libraries are required).

## Usage

Run the program natively from the command line using the required assignment schema:

```bash
python parse.py <grammar_file.gr> <sentences_file.sen>
```

#### Example 1: Testing the Baseline Grammar
```bash
python parse.py time/time.gr time/time.sen
```

#### Example 2: Testing PP-Attachment Ambiguity
```bash
python parse.py soldier/soldier.gr soldier/soldier.sen
```

## Output Formatting
Parsed grammatical structures inherently output dynamically indented nested groupings (Lisp-like S-expressions).
If no viable parse rules complete, the system outputs exactly `NONE`.

```text
(S
  (NP (N time))
  (VP (V flies)
    (ADVP (ADV like)
      (NP (Det an) (N arrow)))))
7.802285552379208
```

*The float following the tree marks the definitive minimum baseline cost derived from `-log_2(P)`.*

## Assignment Documentation
Please refer to `Report.md` in the root mapping directory for structured outlines addressing dynamic tracking bounds, memory constraints, and analytical cost validation bounds required by the initial grading constraints.