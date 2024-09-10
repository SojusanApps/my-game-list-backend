"""This module contains the models for the Platform."""

from typing import ClassVar

from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel


class Platform(BaseDictionaryModel):
    """Data about game platforms."""

    abbreviation = models.CharField(_("abbreviation"), max_length=255, blank=True)
    igdb_id = models.PositiveIntegerField(_("igdb id"), unique=True)

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the platform model."""

        verbose_name = _("platform")
        verbose_name_plural = _("platforms")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["abbreviation"],
                name="unique_abbreviation",
                condition=models.Q(abbreviation__isnull=False, abbreviation__gt=""),
            ),
        ]
