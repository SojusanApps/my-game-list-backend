from .resource import Model as Model
from _typeshed import Incomplete
from docker.api import APIClient as APIClient
from docker.errors import APIError as APIError

class Swarm(Model):
    id_attribute: str
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    @property
    def version(self) -> Incomplete: ...
    def get_unlock_key(self) -> Incomplete: ...
    def init(
        self,
        advertise_addr: Incomplete | None = ...,
        listen_addr: str = ...,
        force_new_cluster: bool = ...,
        default_addr_pool: Incomplete | None = ...,
        subnet_size: Incomplete | None = ...,
        data_path_addr: Incomplete | None = ...,
        data_path_port: Incomplete | None = ...,
        **kwargs: Incomplete
    ) -> Incomplete: ...
    def join(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def leave(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    attrs: Incomplete
    def reload(self) -> None: ...
    def unlock(self, key: Incomplete) -> Incomplete: ...
    def update(
        self,
        rotate_worker_token: bool = ...,
        rotate_manager_token: bool = ...,
        rotate_manager_unlock_key: bool = ...,
        **kwargs: Incomplete
    ) -> Incomplete: ...
