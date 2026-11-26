from dataclasses import dataclass

@dataclass
class Node: pass
@dataclass
class Program(Node): statements: list
@dataclass
class Literal(Node): value: object
@dataclass
class Variable(Node): name: str
@dataclass
class ListExpr(Node): items: list
@dataclass
class Unary(Node): op: str; right: Node
@dataclass
class Binary(Node): left: Node; op: str; right: Node
@dataclass
class Call(Node): name: str; args: list
@dataclass
class Let(Node): name: str; value: Node
@dataclass
class SetVar(Node): name: str; value: Node
@dataclass
class Print(Node): value: Node
@dataclass
class If(Node): condition: Node; yes: list; no: list
@dataclass
class While(Node): condition: Node; body: list
@dataclass
class Function(Node): name: str; params: list; body: list
@dataclass
class Return(Node): value: Node
