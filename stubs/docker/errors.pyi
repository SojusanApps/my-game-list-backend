import requests
from _typeshed import Incomplete

from .models.containers import Container

class DockerException(Exception): ...

def create_api_error_from_http_exception(e: requests.RequestException) -> None: ...

class APIError(requests.exceptions.HTTPError, DockerException):
    response: requests.Response | None
    explanation: str | None
    def __init__(
        self: APIError, message: str, response: requests.Response | None = ..., explanation: str | None = ...
    ) -> None: ...
    @property
    def status_code(self: APIError) -> int | None: ...
    def is_error(self: APIError) -> bool: ...
    def is_client_error(self: APIError) -> bool: ...
    def is_server_error(self: APIError) -> bool: ...

class NotFound(APIError): ...
class ImageNotFound(NotFound): ...
class InvalidVersion(DockerException): ...
class InvalidRepository(DockerException): ...
class InvalidConfigFile(DockerException): ...
class InvalidArgument(DockerException): ...
class DeprecatedMethod(DockerException): ...

class TLSParameterError(DockerException):
    msg: str
    def __init__(self: TLSParameterError, msg: str) -> None: ...

class NullResource(DockerException, ValueError): ...

class ContainerError(DockerException):
    container: Container
    exit_status: int
    command: str
    image: str
    stderr: None
    def __init__(
        self: ContainerError, container: Container, exit_status: int, command: str, image: str, stderr: None
    ) -> None: ...

class StreamParseError(RuntimeError):
    msg: str
    def __init__(self: StreamParseError, reason: str) -> None: ...

class BuildError(DockerException):
    msg: str
    build_log: list[dict[str, str]]
    def __init__(self: BuildError, reason: str, build_log: list[dict[str, str]]) -> None: ...

class ImageLoadError(DockerException): ...

def create_unexpected_kwargs_error(name: Incomplete, kwargs: Incomplete) -> Incomplete: ...

class MissingContextParameter(DockerException):
    param: Incomplete
    def __init__(self, param: Incomplete) -> None: ...

class ContextAlreadyExists(DockerException):
    name: Incomplete
    def __init__(self, name: Incomplete) -> None: ...

class ContextException(DockerException):
    msg: Incomplete
    def __init__(self, msg: Incomplete) -> None: ...

class ContextNotFound(DockerException):
    name: Incomplete
    def __init__(self, name: Incomplete) -> None: ...
