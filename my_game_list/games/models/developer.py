from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel


class Developer(BaseDictionaryModel):
    """Data about developers."""

    class Meta(BaseDictionaryModel.Meta):
        verbose_name = _("developer")
        verbose_name_plural = _("developers")
