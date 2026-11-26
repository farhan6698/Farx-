from .ast_nodes import *
from .errors import FarxError

class ReturnSignal(Exception):
    def __init__(self, value): self.value=value

class Environment:
    def __init__(self, parent=None): self.values={}; self.parent=parent
    def get(self,n):
        if n in self.values: return self.values[n]
        if self.parent: return self.parent.get(n)
        raise FarxError(f"Undefined variable: {n}")
    def set(self,n,v):
        if n in self.values: self.values[n]=v; return
        if self.parent and self.parent.has(n): self.parent.set(n,v); return
        raise FarxError(f"Cannot SET unknown variable: {n}")
    def has(self,n): return n in self.values or bool(self.parent and self.parent.has(n))

class UserFunction:
    def __init__(self,node,closure): self.node,self.closure=node,closure

class Interpreter:
    def __init__(self, output=print, input_fn=input):
        self.output,self.input_fn=output,input_fn
        self.global_env=Environment()
        self.global_env.values.update({
            "LEN": lambda x: len(x),
            "STR": lambda x: str(x),
            "NUM": lambda x: float(x) if "." in str(x) else int(x),
            "TYPE": lambda x: "NULL" if x is None else type(x).__name__.upper(),
            "ABS": abs, "MIN": min, "MAX": max,
            "RANGE": lambda a,b=None: list(range(a)) if b is None else list(range(a,b)),
        })
    def run(self,program): self.exec_block(program.statements,self.global_env)
    def exec_block(self,body,env):
        for s in body: self.exec_stmt(s,env)
    def exec_stmt(self,s,e):
        if isinstance(s,Let): e.values[s.name]=self.eval(s.value,e)
        elif isinstance(s,SetVar): e.set(s.name,self.eval(s.value,e))
        elif isinstance(s,Print): self.output(self.eval(s.value,e))
        elif isinstance(s,If): self.exec_block(s.yes if self.truth(self.eval(s.condition,e)) else s.no,e)
        elif isinstance(s,While):
            count=0
            while self.truth(self.eval(s.condition,e)):
                count+=1
                if count>100000: raise FarxError("Loop safety limit exceeded (100000 iterations)")
                self.exec_block(s.body,e)
        elif isinstance(s,Function): e.values[s.name]=UserFunction(s,e)
        elif isinstance(s,Return): raise ReturnSignal(self.eval(s.value,e))
        else: raise FarxError(f"Unsupported statement: {type(s).__name__}")
    def truth(self,v): return bool(v)
    def eval(self,n,e):
        if isinstance(n,Literal): return n.value
        if isinstance(n,Variable): return e.get(n.name)
        if isinstance(n,ListExpr): return [self.eval(x,e) for x in n.items]
        if isinstance(n,Unary):
            v=self.eval(n.right,e)
            return -v if n.op=="-" else not self.truth(v)
        if isinstance(n,Binary):
            a=self.eval(n.left,e)
            if n.op=="AND": return self.truth(a) and self.truth(self.eval(n.right,e))
            if n.op=="OR": return self.truth(a) or self.truth(self.eval(n.right,e))
            b=self.eval(n.right,e)
            ops={"+":lambda:a+b,"-":lambda:a-b,"*":lambda:a*b,"/":lambda:a/b,"%":lambda:a%b,
                 "==":lambda:a==b,"!=":lambda:a!=b,"<":lambda:a<b,">":lambda:a>b,"<=":lambda:a<=b,">=":lambda:a>=b}
            try: return ops[n.op]()
            except ZeroDivisionError: raise FarxError("Division by zero")
            except (TypeError,KeyError) as ex: raise FarxError(f"Invalid operation {n.op}: {ex}")
        if isinstance(n,Call):
            fn=e.get(n.name); args=[self.eval(x,e) for x in n.args]
            if isinstance(fn,UserFunction):
                if len(args)!=len(fn.node.params): raise FarxError(f"{n.name} expects {len(fn.node.params)} arguments")
                local=Environment(fn.closure); local.values.update(zip(fn.node.params,args))
                try: self.exec_block(fn.node.body,local)
                except ReturnSignal as r: return r.value
                return None
            if callable(fn):
                try: return fn(*args)
                except Exception as ex: raise FarxError(f"Built-in {n.name} failed: {ex}")
            raise FarxError(f"{n.name} is not callable")
        raise FarxError(f"Unsupported expression: {type(n).__name__}")
