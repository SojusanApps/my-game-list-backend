"""This module contains the models for the Game."""

from typing import Self

from django.contrib import admin
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from my_game_list.games.models import Company
from my_game_list.games.models.genre import Genre
from my_game_list.games.models.platform import Platform
from my_game_list.games.querysets import GameQuerySet
from my_game_list.my_game_list.igdb_integration import IGDBImageSize, get_image_url
from my_game_list.my_game_list.models import BaseModel


class Game(BaseModel):
    """A model containing data about games."""

    title = models.CharField(_("title"), max_length=255, unique=True)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)
    release_date = models.DateField(_("release date"), blank=True, null=True)
    cover_image_id = models.CharField(_("cover image id"), max_length=255, blank=True)
    summary = models.TextField(_("summary"), blank=True, max_length=2000)
    igdb_id = models.PositiveIntegerField(_("igdb id"), unique=True)

    publisher = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="games_published",
        blank=True,
        null=True,
    )
    developer = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="games_developed",
        blank=True,
        null=True,
    )
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
        if self.cover_image_id:
            return format_html(
                '<img src={} width="90" height="128">',
                get_image_url(self.cover_image_id, IGDBImageSize.COVER_SMALL_90_128),
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
