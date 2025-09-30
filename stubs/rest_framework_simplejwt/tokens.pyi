from .backends import TokenBackend as TokenBackend
from .exceptions import (
    ExpiredTokenError as ExpiredTokenError,
    TokenBackendError as TokenBackendError,
    TokenBackendExpiredToken as TokenBackendExpiredToken,
    TokenError as TokenError,
)
from .models import TokenUser as TokenUser
from .settings import api_settings as api_settings
from .token_blacklist.models import (
    BlacklistedToken as BlacklistedToken,
    OutstandingToken as OutstandingToken,
)
from .utils import (
    aware_utcnow as aware_utcnow,
    datetime_from_epoch as datetime_from_epoch,
    datetime_to_epoch as datetime_to_epoch,
    format_lazy as format_lazy,
    get_md5_hash_password as get_md5_hash_password,
    logger as logger,
)
from _typeshed import Incomplete
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser
from typing import Any, ClassVar, Generic, TypeVar

T = TypeVar("T", bound="Token")
AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

class Token:
    token_type: str | None
    lifetime: timedelta | None
    token: bytes | None
    current_time: datetime
    payload: dict[str, Any]

    def __init__(self, token: str | bytes | None = None, verify: bool = True) -> None: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
    def get(self, key: str, default: Any | None = None) -> Any: ...
    def verify(self) -> None: ...
    def verify_token_type(self) -> None: ...
    def set_jti(self) -> None: ...
    def set_exp(
        self,
        claim: str = "exp",
        from_time: datetime | None = None,
        lifetime: timedelta | None = None,
    ) -> None: ...
    def set_iat(self, claim: str = "iat", at_time: datetime | None = None) -> None: ...
    def check_exp(self, claim: str = "exp", current_time: datetime | None = None) -> None: ...
    def outstand(self) -> OutstandingToken | None: ...
    @classmethod
    def for_user(cls: type[T], user: AuthUser) -> T: ...
    @property
    def token_backend(self) -> TokenBackend: ...
    def get_token_backend(self) -> TokenBackend: ...

class BlacklistMixin(Generic[T]):
    payload: dict[str, Any]

    def verify(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
    def check_blacklist(self) -> None: ...
    def blacklist(self) -> BlacklistedToken: ...
    def outstand(self) -> OutstandingToken | None: ...
    def for_user(self, user: AuthUser) -> T: ...

class SlidingToken(BlacklistMixin["SlidingToken"], Token):
    token_type: str
    lifetime: timedelta

    def __init__(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...

class AccessToken(Token):
    token_type: str
    lifetime: timedelta

class RefreshToken(BlacklistMixin["RefreshToken"], Token):
    token_type: str
    lifetime: timedelta
    no_copy_claims: ClassVar[tuple[str, ...]]
    access_token_class: type[AccessToken]

    @property
    def access_token(self) -> AccessToken: ...

class UntypedToken(Token):
    token_type: str
    lifetime: timedelta

    def verify_token_type(self) -> None: ...
