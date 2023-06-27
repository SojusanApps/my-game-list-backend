from _typeshed import Incomplete
from docker import errors as errors
from docker.context import Context as Context
from docker.context.config import (
    METAFILE as METAFILE,
    get_current_context_name as get_current_context_name,
    get_meta_dir as get_meta_dir,
    write_context_name_to_docker_config as write_context_name_to_docker_config,
)

class ContextAPI:
    DEFAULT_CONTEXT: Incomplete
    @classmethod
    def create_context(
        cls,
        name: Incomplete,
        orchestrator: Incomplete | None = ...,
        host: Incomplete | None = ...,
        tls_cfg: Incomplete | None = ...,
        default_namespace: Incomplete | None = ...,
        skip_tls_verify: bool = ...,
    ) -> Incomplete: ...
    @classmethod
    def get_context(cls, name: Incomplete | None = ...) -> Incomplete: ...
    @classmethod
    def contexts(cls) -> Incomplete: ...
    @classmethod
    def get_current_context(cls) -> Incomplete: ...
    @classmethod
    def set_current_context(cls, name: str = ...) -> None: ...
    @classmethod
    def remove_context(cls, name: Incomplete) -> None: ...
    @classmethod
    def inspect_context(cls, name: str = ...) -> Incomplete: ...
