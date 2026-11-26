from .tokens import Token, KEYWORDS
from .errors import FarxError

class Lexer:
    def __init__(self, source):
        self.source, self.i, self.line, self.col = source, 0, 1, 1

    def advance(self):
        ch = self.source[self.i]
        self.i += 1
        if ch == "\n": self.line, self.col = self.line + 1, 1
        else: self.col += 1
        return ch

    def peek(self, offset=0):
        p = self.i + offset
        return self.source[p] if p < len(self.source) else "\0"

    def tokens(self):
        out = []
        while self.i < len(self.source):
            ch = self.peek()
            if ch in " \t\r": self.advance(); continue
            if ch == "\n": out.append(Token("NEWLINE", "\n", self.line, self.col)); self.advance(); continue
            if ch == "#":
                while self.peek() not in ("\n", "\0"): self.advance()
                continue
            line, col = self.line, self.col
            if ch.isdigit():
                start = self.i
                while self.peek().isdigit(): self.advance()
                if self.peek() == "." and self.peek(1).isdigit():
                    self.advance()
                    while self.peek().isdigit(): self.advance()
                out.append(Token("NUMBER", float(self.source[start:self.i]) if "." in self.source[start:self.i] else int(self.source[start:self.i]), line, col)); continue
            if ch.isalpha() or ch == "_":
                start = self.i
                while self.peek().isalnum() or self.peek() == "_": self.advance()
                word = self.source[start:self.i]
                upper = word.upper()
                out.append(Token(upper if upper in KEYWORDS else "IDENT", upper if upper in KEYWORDS else word, line, col)); continue
            if ch in "\"'":
                quote = self.advance(); chars = []
                while self.peek() not in (quote, "\0"):
                    c = self.advance()
                    if c == "\\":
                        esc = self.advance()
                        chars.append({"n":"\n", "t":"\t", "r":"\r"}.get(esc, esc))
                    else: chars.append(c)
                if self.peek() == "\0": raise FarxError("Unterminated string", line, col)
                self.advance(); out.append(Token("STRING", "".join(chars), line, col)); continue
            two = ch + self.peek(1)
            if two in ("==", "!=", "<=", ">="):
                self.advance(); self.advance(); out.append(Token(two, two, line, col)); continue
            if ch in "+-*/%()[]=<>,":
                self.advance(); out.append(Token(ch, ch, line, col)); continue
            raise FarxError(f"Unexpected character {ch!r}", line, col)
        out.append(Token("EOF", None, self.line, self.col))
        return out
