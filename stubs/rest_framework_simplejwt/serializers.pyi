from typing import Any, ClassVar, Generic, TypeVar

from django.contrib.auth.models import AbstractBaseUser
from django.utils.functional import _StrPromise
from rest_framework import serializers

from .models import TokenUser as TokenUser
from .settings import api_settings as api_settings
from .token_blacklist.models import BlacklistedToken as BlacklistedToken
from .tokens import (
    RefreshToken as RefreshToken,
    SlidingToken as SlidingToken,
    Token as Token,
    UntypedToken as UntypedToken,
)

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

class PasswordField(serializers.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class TokenObtainSerializer(serializers.Serializer[dict[str, str]], Generic[AuthUser]):
    username_field: str
    token_class: type[Token] | None
    default_error_messages: ClassVar[dict[str, str | _StrPromise]]
    user: AuthUser | None

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]: ...
    @classmethod
    def get_token(cls, user: AuthUser) -> Token: ...

class TokenObtainPairSerializer(TokenObtainSerializer[AuthUser]):
    token_class: type[RefreshToken]

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]: ...

class TokenObtainSlidingSerializer(TokenObtainSerializer[AuthUser]):
    token_class: type[SlidingToken]

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]: ...

class TokenRefreshSerializer(serializers.Serializer[dict[str, str]], Generic[AuthUser]):
    refresh: str
    access: str
    token_class: type[RefreshToken]
    default_error_messages: ClassVar[dict[str, str | _StrPromise]]

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]: ...

class TokenRefreshSlidingSerializer(serializers.Serializer[dict[str, str]]):
    token: str
    token_class: type[SlidingToken]

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]: ...

class TokenVerifySerializer(serializers.Serializer[dict[str, Any]]):
    token: str

    def validate(self, attrs: dict[str, str]) -> dict[str, Any]: ...

class TokenBlacklistSerializer(serializers.Serializer[dict[str, Any]]):
    refresh: str
    token_class: type[RefreshToken]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]: ...
