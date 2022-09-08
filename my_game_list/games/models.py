from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseDictionaryModel, BaseModel


class Publisher(BaseDictionaryModel):
    """Data about publishers."""

    class Meta(BaseDictionaryModel.Meta):
        verbose_name = _("publisher")
        verbose_name_plural = _("publishers")


class Developer(BaseDictionaryModel):
    """Data about developers."""

    class Meta(BaseDictionaryModel.Meta):
        verbose_name = _("developer")
        verbose_name_plural = _("developers")


class Genre(BaseDictionaryModel):
    """Data about game genres."""

    class Meta(BaseDictionaryModel.Meta):
        verbose_name = _("genre")
        verbose_name_plural = _("genres")


class Platform(BaseDictionaryModel):
    """Data about game platforms."""

    class Meta(BaseDictionaryModel.Meta):
        verbose_name = _("platform")
        verbose_name_plural = _("platforms")


class Game(BaseModel):
    """A model containing data about games."""

    title = models.CharField(_("title"), max_length=255, unique=True)
    creation_time = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True)
    release_date = models.DateField(_("release date"), blank=True, null=True)
    cover_image = models.ImageField(_("cover image"), upload_to="cover_images/")
    description = models.TextField(_("description"), blank=True, max_length=2000)

    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="games")
    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, related_name="games")
    genres = models.ManyToManyField(Genre, related_name="games")
    platforms = models.ManyToManyField(Platform, related_name="games")

    class Meta(BaseModel.Meta):
        verbose_name = _("game")
        verbose_name_plural = _("games")

    def __str__(self):
        return self.title


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


class GameFollow(BaseModel):
    """
    Contains the games followed by a user. Following a game means that
    the user wants to have notifications about this game.
    """

    creation_time = models.DateTimeField(_("creation time"), auto_now_add=True)

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="follow_list")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="games_followed"
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("game follow")
        verbose_name_plural = _("games followed")
        constraints = (
            models.UniqueConstraint(
                fields=("game", "user"), name="unique_game_user_in_game_follow"
            ),
        )

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"


class GameReview(BaseModel):
    """Contains reviews for games."""

    score = models.PositiveIntegerField(
        _("score"), validators=[MinValueValidator(1), MaxValueValidator(10)], default=1
    )
    creation_time = models.DateTimeField(_("creation time"), auto_now_add=True)
    review = models.TextField(_("description"), blank=True, max_length=1000)

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="reviews")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reviews"
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("game review")
        verbose_name_plural = _("games reviews")
        constraints = (
            models.UniqueConstraint(
                fields=("game", "user"), name="unique_game_user_in_game_review"
            ),
        )

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
