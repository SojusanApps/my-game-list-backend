import urllib3.connection
from .. import constants as constants
from _typeshed import Incomplete
from docker.transport.basehttpadapter import BaseHTTPAdapter as BaseHTTPAdapter

RecentlyUsedContainer: Incomplete

class UnixHTTPConnection(urllib3.connection.HTTPConnection):
    base_url: Incomplete
    unix_socket: Incomplete
    timeout: Incomplete
    def __init__(self, base_url: Incomplete, unix_socket: Incomplete, timeout: int = ...) -> None: ...
    sock: Incomplete
    def connect(self) -> None: ...

class UnixHTTPConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    base_url: Incomplete
    socket_path: Incomplete
    timeout: Incomplete
    def __init__(
        self, base_url: Incomplete, socket_path: Incomplete, timeout: int = ..., maxsize: int = ...
    ) -> None: ...

class UnixHTTPAdapter(BaseHTTPAdapter):
    __attrs__: Incomplete
    socket_path: Incomplete
    timeout: Incomplete
    max_pool_size: Incomplete
    pools: Incomplete
    def __init__(
        self,
        socket_url: Incomplete,
        timeout: int = ...,
        pool_connections: Incomplete = ...,
        max_pool_size: Incomplete = ...,
    ) -> None: ...
    def get_connection(self, url: Incomplete, proxies: Incomplete | None = ...) -> Incomplete: ...
    def request_url(self, request: Incomplete, proxies: Incomplete) -> Incomplete: ...
