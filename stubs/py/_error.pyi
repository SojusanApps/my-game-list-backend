from _typeshed import Incomplete
from types import ModuleType

class Error(EnvironmentError): ...

class ErrorMaker(ModuleType):
    Error = Error
    def __getattr__(self, name: Incomplete) -> Incomplete: ...
    def checked_call(self, func: Incomplete, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...

error: Incomplete
