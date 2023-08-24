from _typeshed import Incomplete
from builtins import AssertionError as BuiltinAssertionError

class AssertionError(BuiltinAssertionError):
    msg: Incomplete
    args: Incomplete
    def __init__(self, *args: Incomplete) -> None: ...

reinterpret_old: str
