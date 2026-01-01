"""This module contains the models for the game related data."""

from typing import ClassVar, Self

from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
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


class GameEngine(IGDBModel):
    """Data about game engines."""

    name = models.CharField(_("name"), max_length=255)

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the game engine model."""

        verbose_name = _("game engine")
        verbose_name_plural = _("game engines")


class GameMode(BaseDictionaryModel, IGDBModel):
    """Data about game modes."""

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the game mode model."""

        verbose_name = _("game mode")
        verbose_name_plural = _("game modes")


class PlayerPerspective(BaseDictionaryModel, IGDBModel):
    """Data about player perspectives."""

    class Meta(BaseDictionaryModel.Meta):
        """Meta data for the player perspective model."""

        verbose_name = _("player perspective")
        verbose_name_plural = _("player perspectives")


class GameStats(models.Model):
    """Data about game statistics."""

    game = models.OneToOneField("Game", on_delete=models.CASCADE, related_name="stats")

    # Aggregates (Updated via Signals/Save)
    score_sum = models.BigIntegerField(_("score sum"), default=0)
    score_count = models.PositiveIntegerField(_("score count"), default=0)
    average_score = models.DecimalField(
        _("average score"),
        max_digits=4,
        decimal_places=2,
        default=0,
        db_index=True,
    )
    members_count = models.PositiveIntegerField(_("members count"), default=0, db_index=True)

    # Ranks (Updated via Celery)
    popularity = models.PositiveIntegerField(_("popularity"), null=True, db_index=True)
    rank_position = models.PositiveIntegerField(_("rank position"), null=True, db_index=True)

    class Meta(TypedModelMeta):
        """Meta data for the game stats model."""

        verbose_name = _("game stats")
        verbose_name_plural = _("game stats")

    def __str__(self: Self) -> str:
        """String representation of the game stats model."""
        return f"{self.game.title} - Stats"


class GameType(BaseModel, IGDBModel):
    """Data about game types."""

    type = models.CharField(_("type"), max_length=255, unique=True)

    class Meta(BaseModel.Meta):
        """Meta data for the game type model."""

        verbose_name = _("game type")
        verbose_name_plural = _("game types")

    def __str__(self: Self) -> str:
        """String representation of the game type model."""
        return self.type


class GameStatus(BaseModel, IGDBModel):
    """Data about game statuses."""

    status = models.CharField(_("status"), max_length=255, unique=True)

    class Meta(BaseModel.Meta):
        """Meta data for the game status model."""

        verbose_name = _("game status")
        verbose_name_plural = _("game statuses")

    def __str__(self: Self) -> str:
        """String representation of the game status model."""
        return self.status


class Game(BaseModel, IGDBModel):
    """A model containing data about games."""

    title = models.CharField(_("title"), max_length=255)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True, db_index=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)
    release_date = models.DateField(_("release date"), blank=True, null=True)
    cover_image_id = models.CharField(_("cover image id"), max_length=255, blank=True)
    summary = models.TextField(_("summary"), blank=True, max_length=2000)

    game_type = models.ForeignKey(
        GameType,
        on_delete=models.SET_NULL,
        related_name="games",
        blank=True,
        null=True,
    )
    game_status = models.ForeignKey(
        GameStatus,
        on_delete=models.SET_NULL,
        related_name="games",
        blank=True,
        null=True,
    )

    parent_game = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children_games",
    )

    bundles = models.ManyToManyField("self", symmetrical=False, related_name="bundled_in", blank=True)
    dlcs = models.ManyToManyField("self", symmetrical=False, related_name="dlc_of", blank=True)
    expanded_games = models.ManyToManyField("self", symmetrical=False, related_name="expanded_by", blank=True)
    expansions = models.ManyToManyField("self", symmetrical=False, related_name="expansion_of", blank=True)
    forks = models.ManyToManyField("self", symmetrical=False, related_name="fork_of", blank=True)
    ports = models.ManyToManyField("self", symmetrical=False, related_name="port_of", blank=True)
    standalone_expansions = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="standalone_expansion_of",
        blank=True,
    )

    game_engines = models.ManyToManyField(GameEngine, related_name="games", blank=True)
    game_modes = models.ManyToManyField(GameMode, related_name="games", blank=True)
    player_perspectives = models.ManyToManyField(PlayerPerspective, related_name="games", blank=True)
    screenshots = ArrayField(models.CharField(max_length=255), default=list, blank=True)

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

    @property
    def average_score(self: Self) -> float:
        """Annotate the average score for the game."""
        if hasattr(self, "stats"):
            return float(self.stats.average_score)
        return 0.0

    @property
    def scores_count(self: Self) -> int:
        """Annotate the number of all ratings for the game."""
        if hasattr(self, "stats"):
            return self.stats.score_count
        return 0

    @property
    def rank_position(self: Self) -> int:
        """Annotate the rank position of the game. The rank position is calculated based on the average score."""
        if hasattr(self, "stats") and self.stats.rank_position is not None:
            return self.stats.rank_position
        return 0

    @property
    def members_count(self: Self) -> int:
        """Annotate the number of all members for the game."""
        if hasattr(self, "stats"):
            return self.stats.members_count
        return 0

    @property
    def popularity(self: Self) -> int:
        """Annotate the popularity of the game. The popularity is calculated based on the number of members."""
        if hasattr(self, "stats") and self.stats.popularity is not None:
            return self.stats.popularity
        return 0
