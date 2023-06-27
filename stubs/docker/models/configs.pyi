from ..api import APIClient as APIClient
from .resource import Collection as Collection, Model as Model
from _typeshed import Incomplete

class Config(Model):
    id_attribute: str
    @property
    def name(self) -> Incomplete: ...
    def remove(self) -> Incomplete: ...

class ConfigCollection(Collection):
    model = Config
    def create(self, **kwargs: Incomplete) -> Incomplete: ...  # type: ignore[override]
    def get(self, config_id: Incomplete) -> Incomplete: ...
    def list(self, **kwargs: Incomplete) -> Incomplete: ...
