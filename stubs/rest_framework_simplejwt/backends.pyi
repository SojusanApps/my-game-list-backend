import json
from collections.abc import Iterable
from datetime import timedelta
from functools import cached_property
from typing import Any

from .exceptions import (
    TokenBackendError as TokenBackendError,
    TokenBackendExpiredToken as TokenBackendExpiredToken,
)
from .tokens import Token as Token
from .utils import format_lazy as format_lazy

JWK_CLIENT_AVAILABLE: bool
ALLOWED_ALGORITHMS: tuple[str, ...]

class TokenBackend:
    algorithm: str
    signing_key: str | None
    verifying_key: str
    audience: str | list[str] | None
    issuer: str | None
    jwks_client: Any
    leeway: timedelta
    json_encoder: type[json.JSONEncoder] | None

    def __init__(
        self,
        algorithm: str,
        signing_key: str | None = None,
        verifying_key: str = "",
        audience: str | Iterable[str] | None = None,
        issuer: str | None = None,
        jwk_url: str | None = None,
        leeway: float | int | timedelta | None = None,
        json_encoder: type[json.JSONEncoder] | None = None,
    ) -> None: ...
    @cached_property
    def prepared_signing_key(self) -> Any: ...
    @cached_property
    def prepared_verifying_key(self) -> Any: ...
    def get_leeway(self) -> timedelta: ...
    def get_verifying_key(self, token: str) -> Any: ...
    def encode(self, payload: dict[str, Any]) -> str: ...
    def decode(self, token: str, verify: bool = True) -> dict[str, Any]: ...
