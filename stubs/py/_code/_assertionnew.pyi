import ast
from _typeshed import Incomplete

class Failure(Exception):
    cause: Incomplete
    explanation: Incomplete
    def __init__(self, explanation: str = ...) -> None: ...

def interpret(source: Incomplete, frame: Incomplete, should_fail: bool = ...) -> Incomplete: ...
def run(offending_line: Incomplete, frame: Incomplete | None = ...) -> Incomplete: ...
def getfailure(failure: Incomplete) -> Incomplete: ...

operator_map: Incomplete
unary_map: Incomplete

class DebugInterpreter(ast.NodeVisitor):
    frame: Incomplete
    def __init__(self, frame: Incomplete) -> None: ...
    def generic_visit(self, node: Incomplete) -> Incomplete: ...
    def visit_Expr(self, expr: Incomplete) -> Incomplete: ...
    def visit_Module(self, mod: Incomplete) -> None: ...
    def visit_Name(self, name: Incomplete) -> Incomplete: ...
    def visit_Compare(self, comp: Incomplete) -> Incomplete: ...
    def visit_BoolOp(self, boolop: Incomplete) -> Incomplete: ...
    def visit_UnaryOp(self, unary: Incomplete) -> Incomplete: ...
    def visit_BinOp(self, binop: Incomplete) -> Incomplete: ...
    def visit_Call(self, call: Incomplete) -> Incomplete: ...
    def visit_Attribute(self, attr: Incomplete) -> Incomplete: ...
    def visit_Assert(self, assrt: Incomplete) -> Incomplete: ...
    def visit_Assign(self, assign: Incomplete) -> Incomplete: ...