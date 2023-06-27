from .. import errors as errors, types as types, utils as utils
from ..constants import (
    DEFAULT_SWARM_ADDR_POOL as DEFAULT_SWARM_ADDR_POOL,
    DEFAULT_SWARM_SUBNET_SIZE as DEFAULT_SWARM_SUBNET_SIZE,
)
from _typeshed import Incomplete

log: Incomplete

class SwarmApiMixin:
    def create_swarm_spec(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def get_unlock_key(self) -> Incomplete: ...
    def init_swarm(
        self,
        advertise_addr: Incomplete | None = ...,
        listen_addr: str = ...,
        force_new_cluster: bool = ...,
        swarm_spec: Incomplete | None = ...,
        default_addr_pool: Incomplete | None = ...,
        subnet_size: Incomplete | None = ...,
        data_path_addr: Incomplete | None = ...,
        data_path_port: Incomplete | None = ...,
    ) -> Incomplete: ...
    def inspect_swarm(self) -> Incomplete: ...
    def inspect_node(self, node_id: Incomplete) -> Incomplete: ...
    def join_swarm(
        self,
        remote_addrs: Incomplete,
        join_token: Incomplete,
        listen_addr: str = ...,
        advertise_addr: Incomplete | None = ...,
        data_path_addr: Incomplete | None = ...,
    ) -> Incomplete: ...
    def leave_swarm(self, force: bool = ...) -> Incomplete: ...
    def nodes(self, filters: Incomplete | None = ...) -> Incomplete: ...
    def remove_node(self, node_id: Incomplete, force: bool = ...) -> Incomplete: ...
    def unlock_swarm(self, key: Incomplete) -> Incomplete: ...
    def update_node(
        self, node_id: Incomplete, version: Incomplete, node_spec: Incomplete | None = ...
    ) -> Incomplete: ...
    def update_swarm(
        self,
        version: Incomplete,
        swarm_spec: Incomplete | None = ...,
        rotate_worker_token: bool = ...,
        rotate_manager_token: bool = ...,
        rotate_manager_unlock_key: bool = ...,
    ) -> Incomplete: ...
