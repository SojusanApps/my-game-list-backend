from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel


class Genre(BaseDictionaryModel):
    """Data about game genres."""

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the genre model."""

        verbose_name = _("genre")
        verbose_name_plural = _("genres")
