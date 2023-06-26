"""This module contains the models for the GameReview."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.games.models.game import Game
from my_game_list.my_game_list.models import BaseModel


class GameReview(BaseModel):
    """Contains reviews for games."""

    score = models.PositiveIntegerField(_("score"), validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    review = models.TextField(_("description"), blank=True, max_length=1000)

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reviews")

    class Meta(BaseModel.Meta):
        """Meta data for game review model."""

        verbose_name = _("game review")
        verbose_name_plural = _("games reviews")
        constraints = (models.UniqueConstraint(fields=("game", "user"), name="unique_game_user_in_game_review"),)

    def __str__(self: "GameReview") -> str:
        """String representation of the game review model."""
        return f"{self.user.username} - {self.game.title}"
