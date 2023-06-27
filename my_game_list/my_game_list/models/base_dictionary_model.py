"""This module contains the base dictionary model for all dictionary models in the application."""
from typing import Self

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class BaseDictionaryModel(models.Model):
    """Base class for all dictionary models."""

    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta(TypedModelMeta):
        """Meta data for dictionary models."""

        abstract = True
        ordering = ("id",)

    def __str__(self: Self) -> str:
        """String representation of dictionary models."""
        return self.name
