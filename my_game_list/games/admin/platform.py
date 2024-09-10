"""This module contains the admin models for the Platform."""

from django.contrib import admin

from my_game_list.games.models import Platform
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Platform)
class PlatformAdmin(BaseDictionaryModelAdmin):
    """Admin model for the platform model."""

    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields, "igdb_id")
    list_display = (*BaseDictionaryModelAdmin.list_display, "abbreviation", "igdb_id")
