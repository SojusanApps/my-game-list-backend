from .settings import api_settings as api_settings
from .token_blacklist.models import BlacklistedToken as BlacklistedToken
from .tokens import RefreshToken as RefreshToken, SlidingToken as SlidingToken, UntypedToken as UntypedToken
from _typeshed import Incomplete
from typing import Mapping, TypeVar
from rest_framework import serializers
from django.contrib.auth.models import AbstractBaseUser
from .models import TokenUser
from .tokens import Token

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

class PasswordField(serializers.CharField):
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...

class TokenObtainSerializer(serializers.Serializer[Incomplete]):
    username_field: Incomplete
    token_class: Incomplete
    default_error_messages: Incomplete  # type: ignore[misc]
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    user: Incomplete
    def validate(self, attrs: Mapping[str, Incomplete]) -> dict[Incomplete, Incomplete]: ...
    @classmethod
    def get_token(cls, user: AuthUser) -> Token: ...

class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken
    def validate(self, attrs: Mapping[str, Incomplete]) -> dict[str, str]: ...

class TokenObtainSlidingSerializer(TokenObtainSerializer):
    token_class = SlidingToken
    def validate(self, attrs: Mapping[str, Incomplete]) -> dict[str, str]: ...

class TokenRefreshSerializer(serializers.Serializer[Incomplete]):
    refresh: Incomplete
    access: Incomplete
    token_class = RefreshToken
    def validate(self, attrs: Incomplete) -> Incomplete: ...

class TokenRefreshSlidingSerializer(serializers.Serializer[Incomplete]):
    token: Incomplete
    token_class = SlidingToken
    def validate(self, attrs: Incomplete) -> Incomplete: ...

class TokenVerifySerializer(serializers.Serializer[Incomplete]):
    token: Incomplete
    def validate(self, attrs: Incomplete) -> Incomplete: ...

class TokenBlacklistSerializer(serializers.Serializer[Incomplete]):
    refresh: Incomplete
    token_class = RefreshToken
    def validate(self, attrs: Incomplete) -> Incomplete: ...
