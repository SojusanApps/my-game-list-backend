from datetime import datetime
from typing import Any, ClassVar, TypeVar

from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from ..models import TokenUser as TokenUser
from .models import (
    BlacklistedToken as BlacklistedToken,
    OutstandingToken as OutstandingToken,
)

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

class OutstandingTokenAdmin(admin.ModelAdmin[OutstandingToken]):
    list_display: list[Any]
    search_fields: ClassVar[list[Any]]
    ordering: ClassVar[list[Any]]

    def get_queryset(self, request: HttpRequest) -> QuerySet[OutstandingToken]: ...

    actions: list[Any] | None

    def get_readonly_fields(self, request: HttpRequest, obj: OutstandingToken | None = None) -> list[Any]: ...
    def has_add_permission(self, request: HttpRequest) -> bool: ...
    def has_delete_permission(self, request: HttpRequest, obj: OutstandingToken | None = None) -> bool: ...
    def has_change_permission(self, request: HttpRequest, obj: OutstandingToken | None = None) -> bool: ...

class BlacklistedTokenAdmin(admin.ModelAdmin[BlacklistedToken]):
    list_display: list[Any]
    search_fields: ClassVar[list[Any]]
    ordering: ClassVar[list[Any]]

    def get_queryset(self, request: HttpRequest) -> QuerySet[BlacklistedToken]: ...
    def token_jti(self, obj: BlacklistedToken) -> str: ...
    def token_user(self, obj: BlacklistedToken) -> Any: ...
    def token_created_at(self, obj: BlacklistedToken) -> datetime: ...
    def token_expires_at(self, obj: BlacklistedToken) -> datetime: ...
