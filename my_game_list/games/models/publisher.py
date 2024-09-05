"""This module contains the models for the Publisher."""

from typing import Self

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel
from my_game_list.my_game_list.validators import FileSizeValidator


class Publisher(BaseDictionaryModel):
    """Data about publishers."""

    publisher_logo = models.ImageField(
        _("developer logo"),
        upload_to="publisher_logos/",
        blank=True,
        null=True,
        editable=True,
        validators=[FileSizeValidator()],
    )

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the publisher model."""

        verbose_name = _("publisher")
        verbose_name_plural = _("publishers")

    @property
    @admin.display(description="Publisher logo preview")
    def publisher_logo_tag(self: Self) -> str:
        """Used in admin model to have a image preview."""
        if self.publisher_logo:
            return format_html(
                '<img src={} width="250" height="300">',
                self.publisher_logo.url,
            )
        return ""
