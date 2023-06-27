from .. import auth as auth, errors as errors, utils as utils
from ..types import ServiceMode as ServiceMode
from _typeshed import Incomplete

class ServiceApiMixin:
    def create_service(
        self,
        task_template: Incomplete,
        name: Incomplete | None = ...,
        labels: Incomplete | None = ...,
        mode: Incomplete | None = ...,
        update_config: Incomplete | None = ...,
        networks: Incomplete | None = ...,
        endpoint_config: Incomplete | None = ...,
        endpoint_spec: Incomplete | None = ...,
        rollback_config: Incomplete | None = ...,
    ) -> Incomplete: ...
    def inspect_service(self, service: Incomplete, insert_defaults: Incomplete | None = ...) -> Incomplete: ...
    def inspect_task(self, task: Incomplete) -> Incomplete: ...
    def remove_service(self, service: Incomplete) -> Incomplete: ...
    def services(self, filters: Incomplete | None = ..., status: Incomplete | None = ...) -> Incomplete: ...
    def service_logs(
        self,
        service: Incomplete,
        details: bool = ...,
        follow: bool = ...,
        stdout: bool = ...,
        stderr: bool = ...,
        since: int = ...,
        timestamps: bool = ...,
        tail: str = ...,
        is_tty: Incomplete | None = ...,
    ) -> Incomplete: ...
    def tasks(self, filters: Incomplete | None = ...) -> Incomplete: ...
    def update_service(
        self,
        service: Incomplete,
        version: Incomplete,
        task_template: Incomplete | None = ...,
        name: Incomplete | None = ...,
        labels: Incomplete | None = ...,
        mode: Incomplete | None = ...,
        update_config: Incomplete | None = ...,
        networks: Incomplete | None = ...,
        endpoint_config: Incomplete | None = ...,
        endpoint_spec: Incomplete | None = ...,
        fetch_current_spec: bool = ...,
        rollback_config: Incomplete | None = ...,
    ) -> Incomplete: ...
