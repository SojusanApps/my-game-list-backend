from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseDictionaryModel(models.Model):
    """Base class for all dictionary models."""

    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
