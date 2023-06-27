from .. import auth as auth, types as types, utils as utils
from _typeshed import Incomplete

class DaemonApiMixin:
    def df(self) -> Incomplete: ...
    def events(
        self,
        since: Incomplete | None = ...,
        until: Incomplete | None = ...,
        filters: Incomplete | None = ...,
        decode: Incomplete | None = ...,
    ) -> Incomplete: ...
    def info(self) -> Incomplete: ...
    def login(
        self,
        username: Incomplete,
        password: Incomplete | None = ...,
        email: Incomplete | None = ...,
        registry: Incomplete | None = ...,
        reauth: bool = ...,
        dockercfg_path: Incomplete | None = ...,
    ) -> Incomplete: ...
    def ping(self) -> Incomplete: ...
    def version(self, api_version: bool = ...) -> Incomplete: ...
