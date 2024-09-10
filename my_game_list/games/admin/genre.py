"""This module contains the admin models for the Genre."""

from django.contrib import admin

from my_game_list.games.models import Genre
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Genre)
class GenreAdmin(BaseDictionaryModelAdmin):
    """Admin model for the genre model."""

    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields, "igdb_id")
    list_display = (*BaseDictionaryModelAdmin.list_display, "igdb_id")
