from .resource import Collection as Collection, Model as Model
from _typeshed import Incomplete
from docker.errors import (
    InvalidArgument as InvalidArgument,
    create_unexpected_kwargs_error as create_unexpected_kwargs_error,
)
from docker.types import (
    ContainerSpec as ContainerSpec,
    Placement as Placement,
    ServiceMode as ServiceMode,
    TaskTemplate as TaskTemplate,
)

class Service(Model):
    id_attribute: str
    @property
    def name(self) -> Incomplete: ...
    @property
    def version(self) -> Incomplete: ...
    def remove(self) -> Incomplete: ...
    def tasks(self, filters: Incomplete | None = ...) -> Incomplete: ...
    def update(self, **kwargs: Incomplete) -> Incomplete: ...
    def logs(self, **kwargs: Incomplete) -> Incomplete: ...
    def scale(self, replicas: Incomplete) -> Incomplete: ...
    def force_update(self) -> Incomplete: ...

class ServiceCollection(Collection):
    model = Service
    def create(self, image: Incomplete, command: Incomplete | None = ..., **kwargs: Incomplete) -> Incomplete: ...  # type: ignore[override]
    def get(self, service_id: Incomplete, insert_defaults: Incomplete | None = ...) -> Incomplete: ...
    def list(self, **kwargs: Incomplete) -> Incomplete: ...

CONTAINER_SPEC_KWARGS: Incomplete
TASK_TEMPLATE_KWARGS: Incomplete
CREATE_SERVICE_KWARGS: Incomplete
PLACEMENT_KWARGS: Incomplete
