"""This module contains the admin models for the GameList."""

from django.contrib import admin

from my_game_list.games.models import GameList


@admin.register(GameList)
class GameListAdmin(admin.ModelAdmin[GameList]):
    """Admin model for the game list model."""

    readonly_fields = ("id",)
    search_fields = (*readonly_fields, "game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("status", "created_at", "last_modified_at", "score")
    list_display = (*readonly_fields, *list_filter, *raw_id_fields)
