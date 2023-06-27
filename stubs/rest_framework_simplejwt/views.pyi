from . import serializers as serializers
from .authentication import AUTH_HEADER_TYPES as AUTH_HEADER_TYPES
from .exceptions import InvalidToken as InvalidToken, TokenError as TokenError
from .settings import api_settings as api_settings
from .tokens import Token
from typing import Sequence
from _typeshed import Incomplete, Unused
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer, Serializer
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import _PermissionClass

class TokenViewBase(generics.GenericAPIView[Incomplete]):
    permission_classes: Sequence[_PermissionClass]
    authentication_classes: Sequence[type[BaseAuthentication]]
    serializer_class: type[BaseSerializer[Incomplete]] | None
    www_authenticate_realm: str
    def get_serializer_class(self) -> type[BaseSerializer[Incomplete]]: ...
    def get_authenticate_header(self, request: Request) -> str: ...
    def post(self, request: Request, *args: Unused, **kwargs: Unused) -> Response: ...

class TokenObtainPairView(TokenViewBase): ...

token_obtain_pair: Incomplete

class TokenRefreshView(TokenViewBase): ...

token_refresh: Incomplete

class TokenObtainSlidingView(TokenViewBase): ...

token_obtain_sliding: Incomplete

class TokenRefreshSlidingView(TokenViewBase): ...

token_refresh_sliding: Incomplete

class TokenVerifyView(TokenViewBase): ...

token_verify: Incomplete

class TokenBlacklistView(TokenViewBase): ...

token_blacklist: Incomplete
