"""This module contains the admin models for the GameFollow."""

from django.contrib import admin

from my_game_list.games.models import GameFollow


@admin.register(GameFollow)
class GameFollowAdmin(admin.ModelAdmin[GameFollow]):
    """Admin model for the game follow model."""

    readonly_fields = ("id",)
    search_fields = (*readonly_fields, "game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("created_at",)
    list_display = (*readonly_fields, *list_filter, *raw_id_fields)
