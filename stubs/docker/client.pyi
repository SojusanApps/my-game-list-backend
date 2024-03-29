from .api.client import APIClient as APIClient
from .constants import (
    DEFAULT_MAX_POOL_SIZE as DEFAULT_MAX_POOL_SIZE,
    DEFAULT_TIMEOUT_SECONDS as DEFAULT_TIMEOUT_SECONDS,
)
from .models.configs import ConfigCollection as ConfigCollection
from .models.containers import ContainerCollection as ContainerCollection
from .models.images import ImageCollection as ImageCollection
from .models.networks import NetworkCollection as NetworkCollection
from .models.nodes import NodeCollection as NodeCollection
from .models.plugins import PluginCollection as PluginCollection
from .models.secrets import SecretCollection as SecretCollection
from .models.services import ServiceCollection as ServiceCollection
from .models.swarm import Swarm as Swarm
from .models.volumes import VolumeCollection as VolumeCollection
from .utils import kwargs_from_env as kwargs_from_env
from _typeshed import Incomplete

class DockerClient:
    api: Incomplete
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    @classmethod
    def from_env(cls, **kwargs: Incomplete) -> Incomplete: ...
    @property
    def configs(self) -> Incomplete: ...
    @property
    def containers(self) -> Incomplete: ...
    @property
    def images(self) -> Incomplete: ...
    @property
    def networks(self) -> Incomplete: ...
    @property
    def nodes(self) -> Incomplete: ...
    @property
    def plugins(self) -> Incomplete: ...
    @property
    def secrets(self) -> Incomplete: ...
    @property
    def services(self) -> Incomplete: ...
    @property
    def swarm(self) -> Incomplete: ...
    @property
    def volumes(self) -> Incomplete: ...
    def events(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def df(self) -> Incomplete: ...
    def info(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def login(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def ping(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def version(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def close(self) -> Incomplete: ...
    def __getattr__(self, name: Incomplete) -> None: ...

from_env: Incomplete
