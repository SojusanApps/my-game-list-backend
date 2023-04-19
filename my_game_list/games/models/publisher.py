from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel


class Publisher(BaseDictionaryModel):
    """Data about publishers."""

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the publisher model."""

        verbose_name = _("publisher")
        verbose_name_plural = _("publishers")
