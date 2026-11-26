# FARX NEXUS — Language Core

FARX NEXUS is an extensible, independent programming-language prototype.
This release provides a working interpreter core, command-line runner,
examples, tests, documentation, and a structured reference-data corpus.

## Requirements
- Python 3.10 or newer
- No third-party packages required

## Run
```bash
python main.py examples/hello.farx
python main.py examples/control_flow.farx
python -m unittest discover -s tests -v
```

## Current language features
- `MODE CODE` / `END MODE`
- variables: `LET name = expression`
- output: `PRINT expression`
- reassignment: `SET name = expression`
- conditionals: `IF ... THEN ... ELSE ... END IF`
- loops: `WHILE ... DO ... END WHILE`
- functions: `FUNCTION name(arg, ...) ... END FUNCTION`
- return: `RETURN expression`
- calls, arithmetic, comparisons, booleans, strings, lists
- comments beginning with `#`
- helpful line/column diagnostics

## Honest scope
This is a functional language-core prototype, not yet the full FARX vision.
Native Android/Windows/Linux compilers, a visual IDE, 3D/audio engines,
network linker, sandbox/security model, optimizer, and 150+ production modes
are future milestones. `LINK` is reserved syntax in the roadmap, not a
working package downloader.

## Project layout
- `farx/lexer.py` — tokenizer
- `farx/parser.py` — recursive-descent parser
- `farx/runtime.py` — evaluator and environments
- `farx/ast_nodes.py` — AST node definitions
- `data/` — FARX reference catalogue and sample datasets
- `examples/` — runnable programs
- `tests/` — automated tests
