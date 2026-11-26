from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    kind: str
    value: object
    line: int
    column: int

KEYWORDS = {
    "MODE", "CODE", "END", "LET", "SET", "PRINT", "IF", "THEN",
    "ELSE", "WHILE", "DO", "FUNCTION", "RETURN", "TRUE", "FALSE",
    "NULL", "AND", "OR", "NOT"
}
