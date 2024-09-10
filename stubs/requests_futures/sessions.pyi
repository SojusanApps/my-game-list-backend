from concurrent.futures import Future
from typing import Self
from _typeshed import Incomplete

from requests import Session, Response

def wrap(
    self: Incomplete, sup: Incomplete, background_callback: Incomplete, *args_: Incomplete, **kwargs_: Incomplete
) -> Incomplete: ...

PICKLE_ERROR: str

class FuturesSession(Session):
    executor: Incomplete
    session: Incomplete
    def __init__(
        self: Self,
        executor: Incomplete | None = None,
        max_workers: int = 8,
        session: Incomplete | None = None,
        adapter_kwargs: Incomplete | None = None,
        *args: Incomplete,
        **kwargs: Incomplete
    ) -> None: ...
    def request(self: Self, *args: Incomplete, **kwargs: Incomplete) -> Future[Response]: ...  # type: ignore[override]
    def close(self: Self) -> None: ...
    def get(self: Self, url: str, **kwargs: Incomplete) -> Future[Response]: ...  # type: ignore[override]
    def options(self: Self, url: str, **kwargs: Incomplete) -> Future[Response]: ...  # type: ignore[override]
    def head(self: Self, url: str, **kwargs: Incomplete) -> Future[Response]: ...  # type: ignore[override]
    def post(  # type: ignore[override]
        self: Self, url: str, data: Incomplete | None = None, json: Incomplete | None = None, **kwargs: Incomplete
    ) -> Future[Response]: ...
    def put(  # type: ignore[override]
        self: Self, url: str, data: Incomplete | None = None, **kwargs: Incomplete
    ) -> Future[Response]: ...
    def patch(  # type: ignore[override]
        self: Self, url: str, data: Incomplete | None = None, **kwargs: Incomplete
    ) -> Future[Response]: ...
    def delete(self: Self, url: str, **kwargs: Incomplete) -> Future[Response]: ...  # type: ignore[override]
