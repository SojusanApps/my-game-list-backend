"""This module contains the models for the Friendship."""

from collections.abc import Iterable
from typing import ClassVar, Self

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.friendships.managers import FriendshipManager
from my_game_list.my_game_list.models import BaseModel


class Friendship(BaseModel):
    """A model representing the friendship relations of the users."""

    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="_friends")

    objects = FriendshipManager()

    class Meta(BaseModel.Meta):
        """Meta data for the friendship model."""

        verbose_name = _("friendship")
        verbose_name_plural = _("friendships")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=("user", "friend"), name="unique_user_friend"),
        ]

    def __str__(self: Self) -> str:
        """String representation of the friendship model."""
        return f"User: {self.user.username}, Friend: {self.friend.username}"

    def save(  # type: ignore[override]
        self: Self,
        *args: Iterable[str] | str | bool | None,
        **kwargs: Iterable[str] | str | bool | None,
    ) -> None:
        """This method saves the friendship model."""
        if self.user == self.friend:
            raise ValidationError(_("The user cannot befriend himself."))
        super().save(*args, **kwargs)  # type: ignore[arg-type]

    def delete(self: Self, *args: bool | None, **kwargs: bool | None) -> tuple[int, dict[str, int]]:  # noqa: ARG002
        """This method deletes the friendship relationship."""
        user = self.user
        friend = self.friend
        return Friendship.objects.filter(user__in=(user, friend), friend__in=(friend, user)).delete()
