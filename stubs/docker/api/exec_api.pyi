from .. import errors as errors, utils as utils
from ..types import CancellableStream as CancellableStream
from _typeshed import Incomplete

class ExecApiMixin:
    def exec_create(
        self,
        container: Incomplete,
        cmd: Incomplete,
        stdout: bool = ...,
        stderr: bool = ...,
        stdin: bool = ...,
        tty: bool = ...,
        privileged: bool = ...,
        user: str = ...,
        environment: Incomplete | None = ...,
        workdir: Incomplete | None = ...,
        detach_keys: Incomplete | None = ...,
    ) -> Incomplete: ...
    def exec_inspect(self, exec_id: Incomplete) -> Incomplete: ...
    def exec_resize(
        self, exec_id: Incomplete, height: Incomplete | None = ..., width: Incomplete | None = ...
    ) -> None: ...
    def exec_start(
        self,
        exec_id: Incomplete,
        detach: bool = ...,
        tty: bool = ...,
        stream: bool = ...,
        socket: bool = ...,
        demux: bool = ...,
    ) -> Incomplete: ...
