from .. import auth as auth, utils as utils
from _typeshed import Incomplete

class PluginApiMixin:
    def configure_plugin(self, name: Incomplete, options: Incomplete) -> Incomplete: ...
    def create_plugin(self, name: Incomplete, plugin_data_dir: Incomplete, gzip: bool = ...) -> Incomplete: ...
    def disable_plugin(self, name: Incomplete, force: bool = ...) -> Incomplete: ...
    def enable_plugin(self, name: Incomplete, timeout: int = ...) -> Incomplete: ...
    def inspect_plugin(self, name: Incomplete) -> Incomplete: ...
    def pull_plugin(self, remote: Incomplete, privileges: Incomplete, name: Incomplete | None = ...) -> Incomplete: ...
    def plugins(self) -> Incomplete: ...
    def plugin_privileges(self, name: Incomplete) -> Incomplete: ...
    def push_plugin(self, name: Incomplete) -> Incomplete: ...
    def remove_plugin(self, name: Incomplete, force: bool = ...) -> Incomplete: ...
    def upgrade_plugin(self, name: Incomplete, remote: Incomplete, privileges: Incomplete) -> Incomplete: ...
