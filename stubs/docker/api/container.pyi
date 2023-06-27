from .. import errors as errors, utils as utils
from ..constants import DEFAULT_DATA_CHUNK_SIZE as DEFAULT_DATA_CHUNK_SIZE
from ..types import (
    CancellableStream as CancellableStream,
    ContainerConfig as ContainerConfig,
    EndpointConfig as EndpointConfig,
    HostConfig as HostConfig,
    NetworkingConfig as NetworkingConfig,
)
from _typeshed import Incomplete

class ContainerApiMixin:
    def attach(
        self,
        container: Incomplete,
        stdout: bool = ...,
        stderr: bool = ...,
        stream: bool = ...,
        logs: bool = ...,
        demux: bool = ...,
    ) -> Incomplete: ...
    def attach_socket(self, container: Incomplete, params: Incomplete | None = ..., ws: bool = ...) -> Incomplete: ...
    def commit(
        self,
        container: Incomplete,
        repository: Incomplete | None = ...,
        tag: Incomplete | None = ...,
        message: Incomplete | None = ...,
        author: Incomplete | None = ...,
        changes: Incomplete | None = ...,
        conf: Incomplete | None = ...,
    ) -> Incomplete: ...
    def containers(
        self,
        quiet: bool = ...,
        all: bool = ...,
        trunc: bool = ...,
        latest: bool = ...,
        since: Incomplete | None = ...,
        before: Incomplete | None = ...,
        limit: int = ...,
        size: bool = ...,
        filters: Incomplete | None = ...,
    ) -> Incomplete: ...
    def create_container(
        self,
        image: Incomplete,
        command: Incomplete | None = ...,
        hostname: Incomplete | None = ...,
        user: Incomplete | None = ...,
        detach: bool = ...,
        stdin_open: bool = ...,
        tty: bool = ...,
        ports: Incomplete | None = ...,
        environment: Incomplete | None = ...,
        volumes: Incomplete | None = ...,
        network_disabled: bool = ...,
        name: Incomplete | None = ...,
        entrypoint: Incomplete | None = ...,
        working_dir: Incomplete | None = ...,
        domainname: Incomplete | None = ...,
        host_config: Incomplete | None = ...,
        mac_address: Incomplete | None = ...,
        labels: Incomplete | None = ...,
        stop_signal: Incomplete | None = ...,
        networking_config: Incomplete | None = ...,
        healthcheck: Incomplete | None = ...,
        stop_timeout: Incomplete | None = ...,
        runtime: Incomplete | None = ...,
        use_config_proxy: bool = ...,
        platform: Incomplete | None = ...,
    ) -> Incomplete: ...
    def create_container_config(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def create_container_from_config(
        self, config: Incomplete, name: Incomplete | None = ..., platform: Incomplete | None = ...
    ) -> Incomplete: ...
    def create_host_config(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def create_networking_config(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def create_endpoint_config(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def diff(self, container: Incomplete) -> Incomplete: ...
    def export(self, container: Incomplete, chunk_size: Incomplete = ...) -> Incomplete: ...
    def get_archive(
        self, container: Incomplete, path: Incomplete, chunk_size: Incomplete = ..., encode_stream: bool = ...
    ) -> Incomplete: ...
    def inspect_container(self, container: Incomplete) -> Incomplete: ...
    def kill(self, container: Incomplete, signal: Incomplete | None = ...) -> None: ...
    def logs(
        self,
        container: Incomplete,
        stdout: bool = ...,
        stderr: bool = ...,
        stream: bool = ...,
        timestamps: bool = ...,
        tail: str = ...,
        since: Incomplete | None = ...,
        follow: Incomplete | None = ...,
        until: Incomplete | None = ...,
    ) -> Incomplete: ...
    def pause(self, container: Incomplete) -> None: ...
    def port(self, container: Incomplete, private_port: Incomplete) -> Incomplete: ...
    def put_archive(self, container: Incomplete, path: Incomplete, data: Incomplete) -> Incomplete: ...
    def prune_containers(self, filters: Incomplete | None = ...) -> Incomplete: ...
    def remove_container(self, container: Incomplete, v: bool = ..., link: bool = ..., force: bool = ...) -> None: ...
    def rename(self, container: Incomplete, name: Incomplete) -> None: ...
    def resize(self, container: Incomplete, height: Incomplete, width: Incomplete) -> None: ...
    def restart(self, container: Incomplete, timeout: int = ...) -> None: ...
    def start(self, container: Incomplete, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    def stats(
        self,
        container: Incomplete,
        decode: Incomplete | None = ...,
        stream: bool = ...,
        one_shot: Incomplete | None = ...,
    ) -> Incomplete: ...
    def stop(self, container: Incomplete, timeout: Incomplete | None = ...) -> None: ...
    def top(self, container: Incomplete, ps_args: Incomplete | None = ...) -> Incomplete: ...
    def unpause(self, container: Incomplete) -> None: ...
    def update_container(
        self,
        container: Incomplete,
        blkio_weight: Incomplete | None = ...,
        cpu_period: Incomplete | None = ...,
        cpu_quota: Incomplete | None = ...,
        cpu_shares: Incomplete | None = ...,
        cpuset_cpus: Incomplete | None = ...,
        cpuset_mems: Incomplete | None = ...,
        mem_limit: Incomplete | None = ...,
        mem_reservation: Incomplete | None = ...,
        memswap_limit: Incomplete | None = ...,
        kernel_memory: Incomplete | None = ...,
        restart_policy: Incomplete | None = ...,
    ) -> Incomplete: ...
    def wait(
        self, container: Incomplete, timeout: Incomplete | None = ..., condition: Incomplete | None = ...
    ) -> Incomplete: ...
