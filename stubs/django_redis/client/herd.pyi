from ..exceptions import ConnectionInterrupted as ConnectionInterrupted
from .default import DefaultClient as DefaultClient
from _typeshed import Incomplete

class Marker: ...

class HerdClient(DefaultClient):
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    def set(
        self,
        key: Incomplete,
        value: Incomplete,
        timeout: Incomplete = ...,
        version: Incomplete | None = ...,
        client: Incomplete | None = ...,
        nx: bool = ...,
        xx: bool = ...,
    ) -> Incomplete: ...
    def get(
        self,
        key: Incomplete,
        default: Incomplete | None = ...,
        version: Incomplete | None = ...,
        client: Incomplete | None = ...,
    ) -> Incomplete: ...
    def get_many(
        self, keys: Incomplete, version: Incomplete | None = ..., client: Incomplete | None = ...
    ) -> Incomplete: ...
    def set_many(
        self,
        data: Incomplete,
        timeout: Incomplete = ...,
        version: Incomplete | None = ...,
        client: Incomplete | None = ...,
        herd: bool = ...,
    ) -> None: ...
    def incr(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...  # type: ignore[override]
    def decr(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...  # type: ignore[override]
    def touch(
        self,
        key: Incomplete,
        timeout: Incomplete = ...,
        version: Incomplete | None = ...,
        client: Incomplete | None = ...,
    ) -> Incomplete: ...
