"""This module contains the base model class for all models in the application."""
from django.db import models


class BaseModel(models.Model):
    """Base class for all models."""

    class Meta:
        """Meta data for all models."""

        abstract = True
        ordering = ("id",)
