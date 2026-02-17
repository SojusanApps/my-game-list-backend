"""This module contains the models for the collection related data."""

from typing import ClassVar, Self

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseModel


class CollectionVisibility(models.TextChoices):
    """Visibility options for collections."""

    PUBLIC = "PUB", _("Public")
    FRIENDS = "FRI", _("Friends only")
    PRIVATE = "PRI", _("Private")


class CollectionMode(models.TextChoices):
    """Mode options for collections."""

    SOLO = "S", _("Solo")
    COLLABORATIVE = "C", _("Collaborative")


class CollectionType(models.TextChoices):
    """Type options for collections."""

    NORMAL = "NOR", _("Normal")
    RANK = "RNK", _("Ranking")
    TIER = "TIE", _("Tier list")


class Tier(models.TextChoices):
    """Tier options for collection items."""

    S = "S", _("S Tier")
    A = "A", _("A Tier")
    B = "B", _("B Tier")
    C = "C", _("C Tier")
    D = "D", _("D Tier")
    E = "E", _("E Tier")


class Collection(BaseModel):
    """A model representing a game collection.

    A collection is a curated list of games that users can create to organize
    games by theme, ranking, or any other criteria. Collections can be private,
    friends-only, or public, and can optionally allow collaborators to add games.
    """

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, max_length=1000)
    is_favorite = models.BooleanField(_("is favorite"), default=False)
    visibility = models.CharField(
        _("visibility"),
        max_length=3,
        choices=CollectionVisibility.choices,
        default=CollectionVisibility.PRIVATE,
    )
    mode = models.CharField(
        _("mode"),
        max_length=1,
        choices=CollectionMode.choices,
        default=CollectionMode.SOLO,
    )
    type = models.CharField(
        _("type"),
        max_length=3,
        choices=CollectionType.choices,
        default=CollectionType.NORMAL,
    )
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collections",
        verbose_name=_("owner"),
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collaborated_collections",
        blank=True,
        verbose_name=_("collaborators"),
    )

    class Meta(BaseModel.Meta):
        """Meta data for the collection model."""

        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    def __str__(self: Self) -> str:
        """String representation of the collection model."""
        return f"{self.user.username} - {self.name}"


class CollectionItem(BaseModel):
    """A model representing a game within a collection.

    Collection items link games to collections and store additional metadata
    like ranking order, optional tier classification, and justification notes.
    """

    order = models.DecimalField(_("order"), max_digits=20, decimal_places=10, null=True, db_index=True)
    tier = models.CharField(
        _("tier"),
        max_length=1,
        choices=Tier.choices,
        blank=True,
        db_index=True,
    )
    description = models.TextField(_("description"), blank=True, max_length=500)
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("last modified"), auto_now=True)

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("collection"),
    )
    game = models.ForeignKey(
        "games.Game",
        on_delete=models.PROTECT,
        related_name="collection_items",
        verbose_name=_("game"),
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="collection_items_added",
        verbose_name=_("added by"),
    )

    class Meta(BaseModel.Meta):
        """Meta data for the collection item model."""

        verbose_name = _("collection item")
        verbose_name_plural = _("collection items")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=("collection", "game"), name="unique_collection_game"),
        ]

    def __str__(self: Self) -> str:
        """String representation of the collection item model."""
        return f"{self.collection.name} - {self.game.title} (#{self.order})"
