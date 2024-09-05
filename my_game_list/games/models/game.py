"""This module contains the models for the Game."""

from typing import Self

from django.contrib import admin
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from my_game_list.games.models.developer import Developer
from my_game_list.games.models.genre import Genre
from my_game_list.games.models.platform import Platform
from my_game_list.games.models.publisher import Publisher
from my_game_list.games.querysets import GameQuerySet
from my_game_list.my_game_list.models import BaseModel
from my_game_list.my_game_list.validators import FileSizeValidator


class Game(BaseModel):
    """A model containing data about games."""

    title = models.CharField(_("title"), max_length=255, unique=True)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)
    release_date = models.DateField(_("release date"), blank=True, null=True)
    cover_image = models.ImageField(
        _("cover image"),
        upload_to="cover_images/",
        editable=True,
        validators=[FileSizeValidator()],
    )
    description = models.TextField(_("description"), blank=True, max_length=2000)

    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="games")
    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, related_name="games")
    genres = models.ManyToManyField(Genre, related_name="games")
    platforms = models.ManyToManyField(Platform, related_name="games")

    objects = GameQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        """Meta data for the game model."""

        verbose_name = _("game")
        verbose_name_plural = _("games")

    def __str__(self: Self) -> str:
        """String representation of the game model."""
        return self.title

    @property
    @admin.display(description="Cover image preview")
    def cover_image_tag(self: Self) -> str:
        """Used in admin model to have a image preview."""
        if self.cover_image:
            return format_html(
                '<img src={} width="250" height="300">',
                self.cover_image.url,
            )
        return ""

    @cached_property
    def average_score(self: Self) -> float:
        """Annotate the average score for the game."""
        return Game.objects.with_average_score().get(id=self.id).average_score

    @cached_property
    def scores_count(self: Self) -> int:
        """Annotate the number of all ratings for the game."""
        return Game.objects.with_scores_count().get(id=self.id).scores_count

    @cached_property
    def rank_position(self: Self) -> int:
        """Annotate the rank position of the game. The rank position is calculated based on the average score."""
        for game in Game.objects.with_rank_position():
            if game.id == self.id:
                return game.rank_position
        return 0

    @cached_property
    def members_count(self: Self) -> int:
        """Annotate the number of all members for the game."""
        return Game.objects.with_members_count().get(id=self.id).members_count

    @cached_property
    def popularity(self: Self) -> int:
        """Annotate the popularity of the game. The popularity is calculated based on the number of members."""
        for game in Game.objects.with_popularity():
            if game.id == self.id:
                return game.popularity
        return 0
