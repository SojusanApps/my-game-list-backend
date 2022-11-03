from django.conf import settings
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
    """
    A game list model. Contains the list of games for user.
    """

    status = models.CharField(_("status"), max_length=3, choices=GameListStatus.choices)
    creation_time = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True)

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="game_lists")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="game_lists"
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("game list")
        verbose_name_plural = _("game lists")
        constraints = (
            models.UniqueConstraint(fields=("game", "user"), name="unique_game_user_in_game_list"),
        )

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
