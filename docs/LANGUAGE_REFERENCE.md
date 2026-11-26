# FARX Language Reference (NEXUS 0.2)

## Program frame
A program may be wrapped in `MODE CODE` and `END MODE`.

## Values
Numbers, strings, booleans (`TRUE`, `FALSE`), `NULL`, and lists are supported.

## Statements
- `LET score = 100` declares a variable.
- `SET score = score + 1` updates an existing variable.
- `PRINT score` writes a value.
- `IF condition THEN ... ELSE ... END IF` branches.
- `WHILE condition DO ... END WHILE` loops.
- `FUNCTION add(a, b) ... RETURN a+b ... END FUNCTION` declares a function.

## Operators
Arithmetic: `+ - * / %`
Comparison: `== != < > <= >=`
Logic: `AND OR NOT`

## Built-ins
`LEN`, `STR`, `NUM`, `TYPE`, `ABS`, `MIN`, `MAX`, `RANGE`.

## Safety
The interpreter limits a single while-loop to 100,000 iterations. Do not run
untrusted source in a process that has access to sensitive files or secrets.
