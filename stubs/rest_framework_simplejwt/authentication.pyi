from .exceptions import (
    AuthenticationFailed as AuthenticationFailed,
    InvalidToken as InvalidToken,
    TokenError as TokenError,
)
from .settings import api_settings as api_settings
from _typeshed import Incomplete
from rest_framework import authentication

AUTH_HEADER_TYPES: Incomplete
AUTH_HEADER_TYPE_BYTES: Incomplete

class JWTAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm: str
    media_type: str
    user_model: Incomplete
    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    def authenticate(self, request: Incomplete) -> Incomplete: ...
    def authenticate_header(self, request: Incomplete) -> Incomplete: ...
    def get_header(self, request: Incomplete) -> Incomplete: ...
    def get_raw_token(self, header: Incomplete) -> Incomplete: ...
    def get_validated_token(self, raw_token: Incomplete) -> Incomplete: ...
    def get_user(self, validated_token: Incomplete) -> Incomplete: ...

class JWTStatelessUserAuthentication(JWTAuthentication):
    def get_user(self, validated_token: Incomplete) -> Incomplete: ...

JWTTokenUserAuthentication = JWTStatelessUserAuthentication

def default_user_authentication_rule(user: Incomplete) -> Incomplete: ...
