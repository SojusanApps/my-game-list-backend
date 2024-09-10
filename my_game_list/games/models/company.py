"""This module contains the models for the Company."""

from typing import Self

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.igdb_integration import IGDBImageSize, get_image_url
from my_game_list.my_game_list.models import BaseDictionaryModel


class Company(BaseDictionaryModel):
    """Data about company."""

    name = models.CharField(_("name"), max_length=255)
    company_logo_id = models.CharField(_("company logo id"), max_length=255, blank=True)
    igdb_id = models.PositiveIntegerField(_("igdb id"), unique=True)

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the company model."""

        verbose_name = _("company")
        verbose_name_plural = _("companies")

    @property
    @admin.display(description="Company logo preview")
    def company_logo_tag(self: Self) -> str:
        """Used in admin model to have a image preview."""
        if self.company_logo_id:
            return format_html(
                '<img src={} width="284" height="160">',
                get_image_url(self.company_logo_id, IGDBImageSize.LOGO_MED_284_160),
            )
        return ""
