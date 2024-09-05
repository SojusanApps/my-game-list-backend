"""This module contains the models for the GameList."""

from typing import ClassVar, Self

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.games.models.game import Game
from my_game_list.my_game_list.models import BaseModel


class GameListStatus(models.TextChoices):
    """Statuses for games in a game list."""

    COMPLETED = "C", _("Completed")
    PLAN_TO_PLAY = "PTP", _("Plan to play")
    PLAYING = "P", _("Playing")
    DROPPED = "D", _("Dropped")
    ON_HOLD = "OH", _("On hold")


class GameList(BaseModel):
    """A game list model. Contains the list of games for user."""

    score = models.PositiveIntegerField(
        _("score"),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
    )
    status = models.CharField(_("status"), max_length=3, choices=GameListStatus.choices)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="game_lists")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="game_lists")

    class Meta(BaseModel.Meta):
        """Meta data for game list model."""

        verbose_name = _("game list")
        verbose_name_plural = _("game lists")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=("game", "user"), name="unique_game_user_in_game_list"),
        ]

    def __str__(self: Self) -> str:
        """String representation of the game list model."""
        return f"{self.user.username} - {self.game.title}"
