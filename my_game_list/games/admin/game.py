"""This module contains the admin models for the Game."""
from typing import Any, ClassVar

from django.contrib import admin
from django.db import models

from my_game_list.games.models import Game
from my_game_list.my_game_list.forms import BinaryFieldWithUpload


class GameInline(admin.StackedInline[Any, Game]):
    """Game inline representation used in related admin models."""

    raw_id_fields = ("publisher",)
    extra = 0
    model = Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin[Game]):
    """Admin model for the game model."""

    formfield_overrides: ClassVar[dict[type[models.Field[Any, Any]], dict[str, Any]]] = {  # type: ignore[misc]
        models.BinaryField: {
            "form_class": BinaryFieldWithUpload,
        },
    }
    readonly_fields = ("id", "cover_image_tag")
    search_fields = (
        "id",
        "title",
        "publisher__name",
        "developer__name",
        "genres__name",
        "platforms__name",
    )
    raw_id_fields = ("publisher", "developer")
    list_filter = ("created_at", "last_modified_at", "release_date")
    list_display = (*readonly_fields, *list_filter, *raw_id_fields, "title", "cover_image")
