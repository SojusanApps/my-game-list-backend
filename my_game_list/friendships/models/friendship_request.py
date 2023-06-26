"""This module contains the model for the FriendshipRequest."""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from my_game_list.friendships.models.friendship import Friendship
from my_game_list.my_game_list.exceptions import ConflictException
from my_game_list.my_game_list.models import BaseModel


class FriendshipRequest(BaseModel):
    """A model contains friendship requests."""

    message = models.CharField(_("message"), max_length=100, blank=True)
    rejected_at = models.DateTimeField(_("rejection time"), blank=True, null=True)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_friend_requests")
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
    )

    class Meta(BaseModel.Meta):
        """Meta data for the friendship request model."""

        verbose_name = _("friendship request")
        verbose_name_plural = _("friendship requests")
        constraints = (models.UniqueConstraint(fields=("sender", "receiver"), name="unique_sender_receiver"),)

    def __str__(self: "FriendshipRequest") -> str:
        """String representation of the friendship request model."""
        return f"From: {self.sender.username} To: {self.receiver.username}"

    def accept(self: "FriendshipRequest") -> bool:
        """Accept this friendship request.

        Returns:
            bool: True after successful operation.
        """
        Friendship.objects.create(user=self.sender, friend=self.receiver)
        Friendship.objects.create(user=self.receiver, friend=self.sender)
        self.delete()

        return True

    def reject(self: "FriendshipRequest") -> bool:
        """Reject this friendship request.

        Returns:
            bool: True after successful operation.
        """
        if self.rejected_at is not None:
            raise ConflictException(_("This friendship request is already rejected."))
        self.rejected_at = timezone.now()
        self.save()

        return True
