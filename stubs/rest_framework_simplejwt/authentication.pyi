from typing import Any, Generic, TypeVar

from django.contrib.auth.models import AbstractBaseUser
from rest_framework import authentication
from rest_framework.request import Request

from .exceptions import (
    AuthenticationFailed as AuthenticationFailed,
    InvalidToken as InvalidToken,
    TokenError as TokenError,
)
from .models import TokenUser as TokenUser
from .settings import api_settings as api_settings
from .tokens import Token as Token
from .utils import get_md5_hash_password as get_md5_hash_password

AUTH_HEADER_TYPES: tuple[str, ...]
AUTH_HEADER_TYPE_BYTES: set[bytes]
AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

class JWTAuthentication(authentication.BaseAuthentication, Generic[AuthUser]):
    www_authenticate_realm: str
    media_type: str
    user_model: type[AuthUser]

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def authenticate(self, request: Request) -> tuple[AuthUser, Token] | None: ...
    def authenticate_header(self, request: Request) -> str: ...
    def get_header(self, request: Request) -> bytes | None: ...
    def get_raw_token(self, header: bytes) -> bytes | None: ...
    def get_validated_token(self, raw_token: bytes) -> Token: ...
    def get_user(self, validated_token: Token) -> AuthUser: ...

class JWTStatelessUserAuthentication(JWTAuthentication[AuthUser]):
    def get_user(self, validated_token: Token) -> AuthUser: ...

JWTTokenUserAuthentication = JWTStatelessUserAuthentication

def default_user_authentication_rule(user: AuthUser | None) -> bool: ...
