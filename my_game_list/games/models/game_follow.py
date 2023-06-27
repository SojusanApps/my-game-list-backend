"""This module contains the models for the GameFollow."""
from typing import ClassVar, Self

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.games.models.game import Game
from my_game_list.my_game_list.models import BaseModel


class GameFollow(BaseModel):
    """Game follow model.

    Contains the games followed by a user. Following a game means that
    the user wants to have notifications about this game.
    """

    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="follow_list")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="games_followed")

    class Meta(BaseModel.Meta):
        """Meta data for the game follow model."""

        verbose_name = _("game follow")
        verbose_name_plural = _("games followed")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=("game", "user"), name="unique_game_user_in_game_follow"),
        ]

    def __str__(self: Self) -> str:
        """String representation of the game follow model."""
        return f"{self.user.username} - {self.game.title}"
