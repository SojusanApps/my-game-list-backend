from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseModel


class FriendList(BaseModel):
    """A model representing the friendship relations of the users."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="friend_list"
    )
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    class Meta(BaseModel.Meta):
        verbose_name = _("friend list")
        verbose_name_plural = _("friend lists")

    def __str__(self):
        return self.user.username
