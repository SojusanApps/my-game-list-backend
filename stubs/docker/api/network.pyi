from .. import utils as utils
from ..errors import InvalidVersion as InvalidVersion
from ..utils import check_resource as check_resource, minimum_version as minimum_version, version_lt as version_lt
from _typeshed import Incomplete

class NetworkApiMixin:
    def networks(
        self, names: Incomplete | None = ..., ids: Incomplete | None = ..., filters: Incomplete | None = ...
    ) -> Incomplete: ...
    def create_network(
        self,
        name: Incomplete,
        driver: Incomplete | None = ...,
        options: Incomplete | None = ...,
        ipam: Incomplete | None = ...,
        check_duplicate: Incomplete | None = ...,
        internal: bool = ...,
        labels: Incomplete | None = ...,
        enable_ipv6: bool = ...,
        attachable: Incomplete | None = ...,
        scope: Incomplete | None = ...,
        ingress: Incomplete | None = ...,
    ) -> Incomplete: ...
    def prune_networks(self, filters: Incomplete | None = ...) -> Incomplete: ...
    def remove_network(self, net_id: Incomplete) -> None: ...
    def inspect_network(
        self, net_id: Incomplete, verbose: Incomplete | None = ..., scope: Incomplete | None = ...
    ) -> Incomplete: ...
    def connect_container_to_network(
        self,
        container: Incomplete,
        net_id: Incomplete,
        ipv4_address: Incomplete | None = ...,
        ipv6_address: Incomplete | None = ...,
        aliases: Incomplete | None = ...,
        links: Incomplete | None = ...,
        link_local_ips: Incomplete | None = ...,
        driver_opt: Incomplete | None = ...,
        mac_address: Incomplete | None = ...,
    ) -> None: ...
    def disconnect_container_from_network(
        self, container: Incomplete, net_id: Incomplete, force: bool = ...
    ) -> None: ...
