import socket
import urllib3.connection
from .. import constants as constants
from _typeshed import Incomplete
from docker.transport.basehttpadapter import BaseHTTPAdapter as BaseHTTPAdapter

RecentlyUsedContainer: Incomplete

class SSHSocket(socket.socket):
    host: Incomplete
    port: Incomplete
    user: Incomplete
    proc: Incomplete
    def __init__(self, host: Incomplete) -> None: ...
    def connect(self, **kwargs: Incomplete) -> None: ...  # type: ignore[override]
    def sendall(self, data: Incomplete) -> None: ...  # type: ignore[override]
    def send(self, data: Incomplete) -> Incomplete: ...  # type: ignore[override]
    def recv(self, n: Incomplete) -> Incomplete: ...  # type: ignore[override]
    def makefile(self, mode: Incomplete) -> Incomplete: ...  # type: ignore[override]
    def close(self) -> None: ...

class SSHConnection(urllib3.connection.HTTPConnection):
    ssh_transport: Incomplete
    timeout: Incomplete
    ssh_host: Incomplete
    def __init__(
        self, ssh_transport: Incomplete | None = ..., timeout: int = ..., host: Incomplete | None = ...
    ) -> None: ...
    sock: Incomplete
    def connect(self) -> None: ...

class SSHConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    scheme = "ssh"
    ssh_transport: Incomplete
    timeout: Incomplete
    ssh_host: Incomplete
    def __init__(
        self, ssh_client: Incomplete | None = ..., timeout: int = ..., maxsize: int = ..., host: Incomplete | None = ...
    ) -> None: ...

class SSHHTTPAdapter(BaseHTTPAdapter):
    __attrs__: Incomplete
    ssh_client: Incomplete
    ssh_host: Incomplete
    timeout: Incomplete
    max_pool_size: Incomplete
    pools: Incomplete
    def __init__(
        self,
        base_url: Incomplete,
        timeout: int = ...,
        pool_connections: Incomplete = ...,
        max_pool_size: Incomplete = ...,
        shell_out: bool = ...,
    ) -> None: ...
    def get_connection(self, url: Incomplete, proxies: Incomplete | None = ...) -> Incomplete: ...
    def close(self) -> None: ...
