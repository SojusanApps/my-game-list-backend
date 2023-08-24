import ast
from _typeshed import Incomplete
from collections.abc import Generator
from builtins import AssertionError as BuiltinAssertionError

passthroughex: Incomplete

class Failure:
    node: Incomplete
    def __init__(self, node: Incomplete) -> None: ...

class View:
    __view__: Incomplete
    __obj__: Incomplete
    __rootclass__: Incomplete
    __class__: Incomplete
    def __new__(rootclass: Incomplete, obj: Incomplete, *args: Incomplete, **kwds: Incomplete) -> Incomplete: ...
    def __getattr__(self, attr: Incomplete) -> Incomplete: ...
    def __viewkey__(self) -> Incomplete: ...
    def __matchkey__(self, key: Incomplete, subclasses: Incomplete) -> Incomplete: ...

def enumsubclasses(cls: Incomplete) -> Generator[Incomplete, None, None]: ...

class Interpretable(View):
    explanation: Incomplete
    def is_builtin(self, frame: Incomplete) -> Incomplete: ...
    result: Incomplete
    def eval(self, frame: Incomplete) -> None: ...
    def run(self, frame: Incomplete) -> None: ...
    def nice_explanation(self) -> Incomplete: ...

class Name(Interpretable):
    __view__: Incomplete
    def is_local(self, frame: Incomplete) -> Incomplete: ...
    def is_global(self, frame: Incomplete) -> Incomplete: ...
    def is_builtin(self, frame: Incomplete) -> Incomplete: ...
    explanation: Incomplete
    def eval(self, frame: Incomplete) -> None: ...

class Compare(Interpretable):
    __view__: Incomplete
    explanation: Incomplete
    result: Incomplete
    def eval(self, frame: Incomplete) -> None: ...

class And(Interpretable):
    __view__: Incomplete
    result: Incomplete
    explanation: Incomplete
    def eval(self, frame: Incomplete) -> None: ...

class Or(Interpretable):
    __view__: Incomplete
    result: Incomplete
    explanation: Incomplete
    def eval(self, frame: Incomplete) -> None: ...

keepalive: Incomplete

class UnaryArith(Interpretable):
    __view__ = ast.IsNot | ast.Invert
    explanation: Incomplete
    result: Incomplete
    def eval(self, frame: Incomplete, astpattern: Incomplete = ...) -> None: ...

class BinaryArith(Interpretable):
    __view__ = ast.Add | ast.Sub | ast.Mult | ast.Div | ast.Mod | ast.Pow
    explanation: Incomplete
    result: Incomplete
    def eval(self, frame: Incomplete, astpattern: Incomplete = ...) -> None: ...

class CallFunc(Interpretable):
    __view__: Incomplete
    def is_bool(self, frame: Incomplete) -> Incomplete: ...
    explanation: Incomplete
    result: Incomplete
    def eval(self, frame: Incomplete) -> None: ...

class Getattr(Interpretable):
    __view__: Incomplete
    result: Incomplete
    explanation: Incomplete
    def eval(self, frame: Incomplete) -> None: ...

class Assert(Interpretable):
    __view__: Incomplete
    result: Incomplete
    explanation: Incomplete
    def run(self, frame: Incomplete) -> None: ...

class Assign(Interpretable):
    __view__: Incomplete
    result: Incomplete
    explanation: Incomplete
    def run(self, frame: Incomplete) -> None: ...

class Discard(Interpretable):
    __view__: Incomplete
    result: Incomplete
    explanation: Incomplete
    def run(self, frame: Incomplete) -> None: ...

class Stmt(Interpretable):
    __view__: Incomplete
    def run(self, frame: Incomplete) -> None: ...

def report_failure(e: Incomplete) -> None: ...
def check(s: Incomplete, frame: Incomplete | None = ...) -> None: ...
def interpret(source: Incomplete, frame: Incomplete, should_fail: bool = ...) -> Incomplete: ...
def getmsg(excinfo: Incomplete) -> Incomplete: ...
def getfailure(e: Incomplete) -> Incomplete: ...
def run(s: Incomplete, frame: Incomplete | None = ...) -> None: ...
