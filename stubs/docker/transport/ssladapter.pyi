import urllib3
from _typeshed import Incomplete
from docker.transport.basehttpadapter import BaseHTTPAdapter as BaseHTTPAdapter

PoolManager = urllib3.poolmanager.PoolManager

class SSLHTTPAdapter(BaseHTTPAdapter):
    __attrs__: Incomplete
    ssl_version: Incomplete
    assert_hostname: Incomplete
    assert_fingerprint: Incomplete
    def __init__(
        self,
        ssl_version: Incomplete | None = ...,
        assert_hostname: Incomplete | None = ...,
        assert_fingerprint: Incomplete | None = ...,
        **kwargs: Incomplete
    ) -> None: ...
    poolmanager: Incomplete
    def init_poolmanager(self, connections: Incomplete, maxsize: Incomplete, block: bool = ...) -> None: ...  # type: ignore[override]
    def get_connection(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def can_override_ssl_version(self) -> Incomplete: ...
