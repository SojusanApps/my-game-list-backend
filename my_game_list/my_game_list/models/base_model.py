from django.db import models


class BaseModel(models.Model):
    """Base class for all models."""

    class Meta:
        """Meta data for all models."""

        abstract = True
