"""This module contains the admin models for the Game."""
from django.contrib import admin

from my_game_list.games.models import Game


class GameInline(admin.StackedInline):
    """Game inline representation used in related admin models."""

    raw_id_fields = ("publisher",)
    extra = 0
    model = Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Admin model for the game model."""

    readonly_fields = ("id",)
    search_fields = readonly_fields + (
        "title",
        "publisher__name",
        "developer__name",
        "genres__name",
        "platforms__name",
    )
    raw_id_fields = ("publisher", "developer")
    list_filter = ("created_at", "last_modified_at", "release_date")
    list_display = readonly_fields + list_filter + raw_id_fields + ("title", "cover_image")
