"""This module contains the models for the game related data."""

from typing import ClassVar, Self

from django.conf import settings
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from my_game_list.games.querysets import GameQuerySet
from my_game_list.my_game_list.igdb_integration import IGDBImageSize, get_image_url
from my_game_list.my_game_list.models import BaseDictionaryModel, BaseModel


class IGDBModel(models.Model):
    """Base IGDB model.

    The IGDB models have an igdb_id field that stores the ID of the object in IGDB
    and an igdb_updated_at field that stores the last time the object was updated in IGDB.
    The `updated_at` field can be used to determine if the object needs to be updated
    from IGDB or not.
    """

    igdb_id = models.PositiveIntegerField(_("igdb id"), unique=True)
    igdb_updated_at = models.DateTimeField(_("igdb last updated at"))

    class Meta(TypedModelMeta):
        """Meta data for dictionary models."""

        abstract = True

    def __str__(self: Self) -> str:
        """String representation of dictionary models."""
        return f"{self.igdb_id}"


class Company(BaseDictionaryModel, IGDBModel):
    """Data about company."""

    name = models.CharField(_("name"), max_length=255)
    company_logo_id = models.CharField(_("company logo id"), max_length=255, blank=True)

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the company model."""

        verbose_name = _("company")
        verbose_name_plural = _("companies")

    @property
    @admin.display(description="Company logo preview")
    def company_logo_tag(self: Self) -> str:
        """Used in admin model to have a image preview."""
        if self.company_logo_id:
            return format_html(
                '<img src={} width="284" height="160">',
                get_image_url(self.company_logo_id, IGDBImageSize.LOGO_MED_284_160),
            )
        return ""


class GameFollow(BaseModel):
    """Game follow model.

    Contains the games followed by a user. Following a game means that
    the user wants to have notifications about this game.
    """

    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)

    game = models.ForeignKey("Game", on_delete=models.PROTECT, related_name="follow_list")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="games_followed",
    )

    class Meta(BaseModel.Meta):
        """Meta data for the game follow model."""

        verbose_name = _("game follow")
        verbose_name_plural = _("games follows")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=("game", "user"), name="unique_game_user_in_game_follow"),
        ]

    def __str__(self: Self) -> str:
        """String representation of the game follow model."""
        return f"{self.user.username} - {self.game.title}"


class GameListStatus(models.TextChoices):
    """Statuses for games in a game list."""

    COMPLETED = "C", _("Completed")
    PLAN_TO_PLAY = "PTP", _("Plan to play")
    PLAYING = "P", _("Playing")
    DROPPED = "D", _("Dropped")
    ON_HOLD = "OH", _("On hold")


class GameMedia(BaseDictionaryModel):
    """Data about media on which the game is owned."""

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the game owned on model."""

        verbose_name = _("game media")
        verbose_name_plural = _("game medias")


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

    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="game_lists")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_lists")
    owned_on = models.ManyToManyField(GameMedia, related_name="game_lists")

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


class GameReview(BaseModel):
    """Contains reviews for games."""

    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    review = models.TextField(_("review"), blank=True, max_length=1000)

    game = models.ForeignKey("Game", on_delete=models.PROTECT, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reviews")

    class Meta(BaseModel.Meta):
        """Meta data for game review model."""

        verbose_name = _("game review")
        verbose_name_plural = _("games reviews")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=("game", "user"), name="unique_game_user_in_game_review"),
        ]

    def __str__(self: Self) -> str:
        """String representation of the game review model."""
        return f"{self.user.username} - {self.game.title}"


class Genre(BaseDictionaryModel, IGDBModel):
    """Data about game genres."""

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the genre model."""

        verbose_name = _("genre")
        verbose_name_plural = _("genres")


class Platform(BaseDictionaryModel, IGDBModel):
    """Data about game platforms."""

    abbreviation = models.CharField(_("abbreviation"), max_length=255, blank=True)

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the platform model."""

        verbose_name = _("platform")
        verbose_name_plural = _("platforms")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["abbreviation"],
                name="unique_abbreviation",
                condition=models.Q(abbreviation__isnull=False, abbreviation__gt=""),
            ),
        ]


class Game(BaseModel, IGDBModel):
    """A model containing data about games."""

    title = models.CharField(_("title"), max_length=255)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)
    release_date = models.DateField(_("release date"), blank=True, null=True)
    cover_image_id = models.CharField(_("cover image id"), max_length=255, blank=True)
    summary = models.TextField(_("summary"), blank=True, max_length=2000)

    publisher = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="games_published",
        blank=True,
        null=True,
    )
    developer = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
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
