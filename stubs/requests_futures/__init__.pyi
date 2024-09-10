import logging
from typing import Self
from _typeshed import Incomplete

__version__: str
__build__: int

class NullHandler(logging.Handler):
    def emit(self: Self, record: Incomplete) -> None: ...
