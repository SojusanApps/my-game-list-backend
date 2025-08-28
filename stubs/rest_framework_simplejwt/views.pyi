from typing import Any, Type

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .authentication import AUTH_HEADER_TYPES as AUTH_HEADER_TYPES
from .exceptions import InvalidToken as InvalidToken, TokenError as TokenError
from .settings import api_settings as api_settings

class TokenViewBase(APIView):
    permission_classes: tuple[Any, ...]
    authentication_classes: tuple[Any, ...]
    serializer_class: Type[Serializer[Any]]
    www_authenticate_realm: str

    def get_serializer_class(self) -> Type[Serializer[Any]]: ...
    def get_authenticate_header(self, request: Request) -> str: ...
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class TokenObtainPairView(TokenViewBase): ...

token_obtain_pair: Type[TokenObtainPairView]

class TokenRefreshView(TokenViewBase): ...

token_refresh: Type[TokenRefreshView]

class TokenObtainSlidingView(TokenViewBase): ...

token_obtain_sliding: Type[TokenObtainSlidingView]

class TokenRefreshSlidingView(TokenViewBase): ...

token_refresh_sliding: Type[TokenRefreshSlidingView]

class TokenVerifyView(TokenViewBase): ...

token_verify: Type[TokenVerifyView]

class TokenBlacklistView(TokenViewBase): ...

token_blacklist: Type[TokenBlacklistView]
