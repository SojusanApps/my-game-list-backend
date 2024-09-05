"""This module contains the models for the Platform."""

from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel


class Platform(BaseDictionaryModel):
    """Data about game platforms."""

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the platform model."""

        verbose_name = _("platform")
        verbose_name_plural = _("platforms")
