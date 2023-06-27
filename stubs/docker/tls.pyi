from . import errors as errors
from .api.client import APIClient
from .transport import SSLHTTPAdapter as SSLHTTPAdapter

class TLSConfig:
    cert: tuple[str] | None
    ca_cert: str | None
    verify: bool | str | None
    ssl_version: int | None
    assert_hostname: bool | None
    assert_fingerprint: str | None

    def __init__(
        self: TLSConfig,
        client_cert: tuple[str] | None = ...,
        ca_cert: str | None = ...,
        verify: bool | str | None = ...,
        ssl_version: int | None = ...,
        assert_hostname: bool | None = ...,
        assert_fingerprint: str | None = ...,
    ) -> None: ...
    def configure_client(self: TLSConfig, client: APIClient) -> None: ...
