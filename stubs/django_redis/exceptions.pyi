from _typeshed import Incomplete

class ConnectionInterrupted(Exception):
    connection: Incomplete
    def __init__(self, connection: Incomplete, parent: Incomplete | None = ...) -> None: ...

class CompressorError(Exception): ...
