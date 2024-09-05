"""This module contains the base model class for all models in the application."""

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class BaseModel(models.Model):
    """Base class for all models."""

    class Meta(TypedModelMeta):
        """Meta data for all models."""

        abstract = True
        ordering = ("id",)
