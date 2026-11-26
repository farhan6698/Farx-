from .ast_nodes import *
from .errors import FarxError

class Parser:
    def __init__(self, tokens): self.t, self.i = tokens, 0
    def cur(self): return self.t[self.i]
    def at(self, *k): return self.cur().kind in k
    def take(self): x=self.cur(); self.i+=1; return x
    def expect(self, k):
        if not self.at(k): raise FarxError(f"Expected {k}, got {self.cur().kind}", self.cur().line, self.cur().column)
        return self.take()
    def skip_lines(self):
        while self.at("NEWLINE"): self.take()
    def parse(self):
        self.skip_lines()
        if self.at("MODE"):
            self.take(); self.expect("CODE"); self.skip_lines()
            body=self.block({"END"})
            self.expect("END"); self.expect("MODE")
        else: body=self.block({"EOF"})
        self.skip_lines()
        self.expect("EOF")
        return Program(body)
    def block(self, stops):
        body=[]; self.skip_lines()
        while not self.at(*stops, "EOF"):
            body.append(self.statement())
            if not self.at("NEWLINE", *stops, "EOF"):
                c=self.cur(); raise FarxError("Expected end of statement",c.line,c.column)
            self.skip_lines()
        return body
    def statement(self):
        if self.at("LET","SET"):
            op=self.take().kind; name=self.expect("IDENT").value; self.expect("="); v=self.expr()
            return Let(name,v) if op=="LET" else SetVar(name,v)
        if self.at("PRINT"): self.take(); return Print(self.expr())
        if self.at("IF"):
            self.take(); cond=self.expr(); self.expect("THEN"); self.skip_lines()
            yes=self.block({"ELSE","END"})
            no=[]
            if self.at("ELSE"): self.take(); self.skip_lines(); no=self.block({"END"})
            self.expect("END"); self.expect("IF")
            return If(cond,yes,no)
        if self.at("WHILE"):
            self.take(); cond=self.expr(); self.expect("DO"); self.skip_lines()
            body=self.block({"END"}); self.expect("END"); self.expect("WHILE")
            return While(cond,body)
        if self.at("FUNCTION"):
            self.take(); name=self.expect("IDENT").value; self.expect("("); params=[]
            if not self.at(")"):
                params.append(self.expect("IDENT").value)
                while self.at(","): self.take(); params.append(self.expect("IDENT").value)
            self.expect(")"); self.skip_lines(); body=self.block({"END"})
            self.expect("END"); self.expect("FUNCTION")
            return Function(name,params,body)
        if self.at("RETURN"): self.take(); return Return(self.expr())
        c=self.cur(); raise FarxError(f"Unexpected statement {c.kind}",c.line,c.column)
    def expr(self): return self.or_expr()
    def or_expr(self):
        x=self.and_expr()
        while self.at("OR"): op=self.take().kind; x=Binary(x,op,self.and_expr())
        return x
    def and_expr(self):
        x=self.equality()
        while self.at("AND"): op=self.take().kind; x=Binary(x,op,self.equality())
        return x
    def equality(self):
        x=self.compare()
        while self.at("==","!="): op=self.take().kind; x=Binary(x,op,self.compare())
        return x
    def compare(self):
        x=self.term()
        while self.at("<",">","<=",">="): op=self.take().kind; x=Binary(x,op,self.term())
        return x
    def term(self):
        x=self.factor()
        while self.at("+","-"): op=self.take().kind; x=Binary(x,op,self.factor())
        return x
    def factor(self):
        x=self.unary()
        while self.at("*","/","%"): op=self.take().kind; x=Binary(x,op,self.unary())
        return x
    def unary(self):
        if self.at("-","NOT"): op=self.take().kind; return Unary(op,self.unary())
        return self.primary()
    def primary(self):
        t=self.cur()
        if self.at("NUMBER","STRING"): self.take(); return Literal(t.value)
        if self.at("TRUE","FALSE","NULL"):
            self.take(); return Literal({"TRUE":True,"FALSE":False,"NULL":None}[t.kind])
        if self.at("IDENT"):
            name=self.take().value
            if self.at("("):
                self.take(); args=[]
                if not self.at(")"):
                    args.append(self.expr())
                    while self.at(","): self.take(); args.append(self.expr())
                self.expect(")"); return Call(name,args)
            return Variable(name)
        if self.at("("): self.take(); x=self.expr(); self.expect(")"); return x
        if self.at("["):
            self.take(); items=[]
            if not self.at("]"):
                items.append(self.expr())
                while self.at(","): self.take(); items.append(self.expr())
            self.expect("]"); return ListExpr(items)
        raise FarxError(f"Expected expression, got {t.kind}",t.line,t.column)
