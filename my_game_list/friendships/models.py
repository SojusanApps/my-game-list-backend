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


class FriendshipRequest(BaseModel):
    """A model contains friendship requests."""

    message = models.CharField(_("message"), max_length=100, blank=True)
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("The request will be inactive if the request was accepted or rejected."),
    )
    creation_time = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sent_friend_requests"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="received_friend_requests"
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("friendship request")
        verbose_name_plural = _("friendship requests")
        constraints = (
            models.UniqueConstraint(fields=("sender", "receiver"), name="unique_sender_receiver"),
        )

    def __str__(self):
        return f"{self.sender.username} - {self.receiver.username}"
