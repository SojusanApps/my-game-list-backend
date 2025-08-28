from _typeshed import Incomplete
from django.db import models

class OutstandingToken(models.Model):
    id: Incomplete
    user: Incomplete
    jti: Incomplete
    token: Incomplete
    created_at: Incomplete
    expires_at: Incomplete

    class Meta:
        verbose_name: Incomplete
        verbose_name_plural: Incomplete
        abstract: Incomplete
        ordering: Incomplete

class BlacklistedToken(models.Model):
    id: Incomplete
    token: Incomplete
    blacklisted_at: Incomplete

    class Meta:
        verbose_name: Incomplete
        verbose_name_plural: Incomplete
        abstract: Incomplete
