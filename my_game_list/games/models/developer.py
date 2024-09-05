"""This module contains the models for the Developer."""

from typing import Self

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel
from my_game_list.my_game_list.validators import FileSizeValidator


class Developer(BaseDictionaryModel):
    """Data about developers."""

    developer_logo = models.ImageField(
        _("developer logo"),
        upload_to="developer_logos/",
        blank=True,
        null=True,
        editable=True,
        validators=[FileSizeValidator()],
    )

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the developer model."""

        verbose_name = _("developer")
        verbose_name_plural = _("developers")

    @property
    @admin.display(description="Developer logo preview")
    def developer_logo_tag(self: Self) -> str:
        """Used in admin model to have a image preview."""
        if self.developer_logo:
            return format_html(
                '<img src={} width="250" height="300">',
                self.developer_logo.url,
            )
        return ""
