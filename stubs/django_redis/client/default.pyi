from .. import pool as pool
from ..exceptions import CompressorError as CompressorError, ConnectionInterrupted as ConnectionInterrupted
from ..util import CacheKey as CacheKey
from _typeshed import Incomplete
from collections import OrderedDict
from datetime import datetime
from django.core.cache.backends.base import BaseCache
from redis import Redis as Redis
from typing import Any, Dict, Iterator, List, Optional, Union

special_re: Incomplete

def glob_escape(s: str) -> str: ...

class DefaultClient:
    reverse_key: Incomplete
    connection_factory: Incomplete
    def __init__(self, server: Incomplete, params: Dict[str, Any], backend: BaseCache) -> None: ...
    def __contains__(self, key: Any) -> bool: ...
    def get_next_client_index(self, write: bool = ..., tried: Optional[List[int]] = ...) -> int: ...
    def get_client(self, write: bool = ..., tried: Optional[List[int]] = ..., show_index: bool = ...) -> Incomplete: ...
    def connect(self, index: int = ...) -> Redis[Incomplete]: ...
    def disconnect(self, index: int = ..., client: Incomplete | None = ...) -> Incomplete: ...
    def set(
        self,
        key: Any,
        value: Any,
        timeout: Optional[float] = ...,
        version: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
        nx: bool = ...,
        xx: bool = ...,
    ) -> bool: ...
    def incr_version(
        self, key: Any, delta: int = ..., version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...
    ) -> int: ...
    def add(
        self,
        key: Any,
        value: Any,
        timeout: Any = ...,
        version: Optional[Any] = ...,
        client: Optional[Redis[Incomplete]] = ...,
    ) -> bool: ...
    def get(
        self,
        key: Any,
        default: Incomplete | None = ...,
        version: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
    ) -> Any: ...
    def persist(self, key: Any, version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...) -> bool: ...
    def expire(
        self, key: Any, timeout: Incomplete, version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...
    ) -> bool: ...
    def pexpire(
        self, key: Incomplete, timeout: Incomplete, version: Incomplete | None = ..., client: Incomplete | None = ...
    ) -> bool: ...
    def pexpire_at(
        self,
        key: Any,
        when: Union[datetime, int],
        version: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
    ) -> bool: ...
    def expire_at(
        self,
        key: Any,
        when: Union[datetime, int],
        version: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
    ) -> bool: ...
    def lock(
        self,
        key: Incomplete,
        version: Optional[int] = ...,
        timeout: Incomplete | None = ...,
        sleep: float = ...,
        blocking_timeout: Incomplete | None = ...,
        client: Optional[Redis[Incomplete]] = ...,
        thread_local: bool = ...,
    ) -> Incomplete: ...
    def delete(
        self,
        key: Any,
        version: Optional[int] = ...,
        prefix: Optional[str] = ...,
        client: Optional[Redis[Incomplete]] = ...,
    ) -> int: ...
    def delete_pattern(
        self,
        pattern: str,
        version: Optional[int] = ...,
        prefix: Optional[str] = ...,
        client: Optional[Redis[Incomplete]] = ...,
        itersize: Optional[int] = ...,
    ) -> int: ...
    def delete_many(
        self, keys: Incomplete, version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...
    ) -> Incomplete: ...
    def clear(self, client: Optional[Redis[Incomplete]] = ...) -> None: ...
    def decode(self, value: Union[bytes, int]) -> Any: ...
    def encode(self, value: Any) -> Union[bytes, Any]: ...
    def get_many(
        self, keys: Incomplete, version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...
    ) -> OrderedDict[Incomplete, Incomplete]: ...
    def set_many(
        self,
        data: Dict[Any, Any],
        timeout: Optional[float] = ...,
        version: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
    ) -> None: ...
    def incr(
        self,
        key: Any,
        delta: int = ...,
        version: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
        ignore_key_check: bool = ...,
    ) -> int: ...
    def decr(
        self, key: Any, delta: int = ..., version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...
    ) -> int: ...
    def ttl(
        self, key: Any, version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...
    ) -> Optional[int]: ...
    def pttl(
        self, key: Incomplete, version: Incomplete | None = ..., client: Incomplete | None = ...
    ) -> Incomplete: ...
    def has_key(self, key: Any, version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...) -> bool: ...
    def iter_keys(
        self,
        search: str,
        itersize: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
        version: Optional[int] = ...,
    ) -> Iterator[str]: ...
    def keys(
        self, search: str, version: Optional[int] = ..., client: Optional[Redis[Incomplete]] = ...
    ) -> List[Any]: ...
    def make_key(self, key: Any, version: Optional[Any] = ..., prefix: Optional[str] = ...) -> CacheKey: ...
    def make_pattern(self, pattern: str, version: Optional[int] = ..., prefix: Optional[str] = ...) -> CacheKey: ...
    def close(self, **kwargs: Incomplete) -> None: ...
    def do_close_clients(self) -> None: ...
    def touch(
        self,
        key: Any,
        timeout: Optional[float] = ...,
        version: Optional[int] = ...,
        client: Optional[Redis[Incomplete]] = ...,
    ) -> bool: ...