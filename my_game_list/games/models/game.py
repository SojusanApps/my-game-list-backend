"""This module contains the models for the Game."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.games.models.developer import Developer
from my_game_list.games.models.genre import Genre
from my_game_list.games.models.platform import Platform
from my_game_list.games.models.publisher import Publisher
from my_game_list.my_game_list.models import BaseModel


class Game(BaseModel):
    """A model containing data about games."""

    title = models.CharField(_("title"), max_length=255, unique=True)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)
    release_date = models.DateField(_("release date"), blank=True, null=True)
    cover_image = models.BinaryField(_("cover image"), max_length=307200, editable=True)
    description = models.TextField(_("description"), blank=True, max_length=2000)

    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="games")
    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, related_name="games")
    genres = models.ManyToManyField(Genre, related_name="games")
    platforms = models.ManyToManyField(Platform, related_name="games")

    class Meta(BaseModel.Meta):
        """Meta data for the game model."""

        verbose_name = _("game")
        verbose_name_plural = _("games")

    def __str__(self) -> str:
        """String representation of the game model."""
        return self.title
