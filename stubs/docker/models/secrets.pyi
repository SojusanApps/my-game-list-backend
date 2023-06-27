from ..api import APIClient as APIClient
from .resource import Collection as Collection, Model as Model
from _typeshed import Incomplete

class Secret(Model):
    id_attribute: str
    @property
    def name(self) -> Incomplete: ...
    def remove(self) -> Incomplete: ...

class SecretCollection(Collection):
    model = Secret
    def create(self, **kwargs: Incomplete) -> Incomplete: ...  # type: ignore[override]
    def get(self, secret_id: Incomplete) -> Incomplete: ...
    def list(self, **kwargs: Incomplete) -> Incomplete: ...
