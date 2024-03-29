from .. import errors as errors
from .resource import Collection as Collection, Model as Model
from _typeshed import Incomplete
from collections.abc import Generator

class Plugin(Model):
    @property
    def name(self) -> Incomplete: ...
    @property
    def enabled(self) -> Incomplete: ...
    @property
    def settings(self) -> Incomplete: ...
    def configure(self, options: Incomplete) -> None: ...
    def disable(self, force: bool = ...) -> None: ...
    def enable(self, timeout: int = ...) -> None: ...
    def push(self) -> Incomplete: ...
    def remove(self, force: bool = ...) -> Incomplete: ...
    def upgrade(self, remote: Incomplete | None = ...) -> Generator[Incomplete, Incomplete, None]: ...

class PluginCollection(Collection):
    model = Plugin
    def create(self, name: Incomplete, plugin_data_dir: Incomplete, gzip: bool = ...) -> Incomplete: ...  # type: ignore[override]
    def get(self, name: Incomplete) -> Incomplete: ...
    def install(self, remote_name: Incomplete, local_name: Incomplete | None = ...) -> Incomplete: ...
    def list(self) -> Incomplete: ...
