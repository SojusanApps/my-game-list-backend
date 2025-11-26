from _typeshed import Incomplete
from typing import ClassVar
from django.db import models

class OutstandingToken(models.Model):
    id: Incomplete
    user: Incomplete
    jti: Incomplete
    token: Incomplete
    created_at: Incomplete
    expires_at: Incomplete

    class Meta:
        verbose_name: ClassVar[Incomplete]
        verbose_name_plural: ClassVar[Incomplete]
        abstract: ClassVar[Incomplete]
        ordering: ClassVar[Incomplete]

class BlacklistedToken(models.Model):
    id: Incomplete
    token: Incomplete
    blacklisted_at: Incomplete

    class Meta:
        verbose_name: ClassVar[Incomplete]
        verbose_name_plural: ClassVar[Incomplete]
        abstract: ClassVar[Incomplete]
