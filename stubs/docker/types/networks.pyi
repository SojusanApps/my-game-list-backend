from .. import errors as errors
from ..utils import normalize_links as normalize_links, version_lt as version_lt
from _typeshed import Incomplete

class EndpointConfig(dict[Incomplete, Incomplete]):
    def __init__(
        self,
        version: Incomplete,
        aliases: Incomplete | None = ...,
        links: Incomplete | None = ...,
        ipv4_address: Incomplete | None = ...,
        ipv6_address: Incomplete | None = ...,
        link_local_ips: Incomplete | None = ...,
        driver_opt: Incomplete | None = ...,
        mac_address: Incomplete | None = ...,
    ) -> None: ...

class NetworkingConfig(dict[Incomplete, Incomplete]):
    def __init__(self, endpoints_config: Incomplete | None = ...) -> None: ...

class IPAMConfig(dict[Incomplete, Incomplete]):
    def __init__(
        self, driver: str = ..., pool_configs: Incomplete | None = ..., options: Incomplete | None = ...
    ) -> None: ...

class IPAMPool(dict[Incomplete, Incomplete]):
    def __init__(
        self,
        subnet: Incomplete | None = ...,
        iprange: Incomplete | None = ...,
        gateway: Incomplete | None = ...,
        aux_addresses: Incomplete | None = ...,
    ) -> None: ...
