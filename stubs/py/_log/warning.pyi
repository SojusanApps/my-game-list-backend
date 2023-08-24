from _typeshed import Incomplete
from builtins import DeprecationWarning as BuiltinDeprecationWarning

class DeprecationWarning(BuiltinDeprecationWarning):
    msg: Incomplete
    path: Incomplete
    lineno: Incomplete
    def __init__(self, msg: Incomplete, path: Incomplete, lineno: Incomplete) -> None: ...

def warn(msg: Incomplete, stacklevel: int = ..., function: Incomplete | None = ...) -> None: ...
