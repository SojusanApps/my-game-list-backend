"""This module contains the admin models for the Game."""

from django.contrib import admin

from my_game_list.games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin[Game]):
    """Admin model for the game model."""

    readonly_fields = ("id", "cover_image_tag", "cover_image_id", "igdb_id")
    search_fields = (
        "id",
        "title",
        "igdb_id",
        "publisher__name",
        "developer__name",
        "genres__name",
        "platforms__name",
    )
    raw_id_fields = ("publisher", "developer")
    list_filter = ("created_at", "last_modified_at", "release_date")
    list_display = (
        *readonly_fields,
        *list_filter,
        *raw_id_fields,
        "title",
        "cover_image_id",
    )
