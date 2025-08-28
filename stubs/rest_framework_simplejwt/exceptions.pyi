from typing import Any

from rest_framework import exceptions

class TokenError(Exception): ...
class ExpiredTokenError(TokenError): ...
class TokenBackendError(Exception): ...
class TokenBackendExpiredToken(TokenBackendError): ...

class DetailDictMixin:
    default_code: str

    def __init__(self, detail: dict[str, Any] | str | None = None, code: str | None = None) -> None: ...

class AuthenticationFailed(DetailDictMixin, exceptions.AuthenticationFailed): ...

class InvalidToken(AuthenticationFailed):
    status_code: int
    default_detail: str
    default_code: str
