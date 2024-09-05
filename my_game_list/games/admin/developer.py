"""This module contains the admin models for the Developer."""

from django.contrib import admin

from my_game_list.games.admin.game import GameInline
from my_game_list.games.models import Developer
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Developer)
class DeveloperAdmin(BaseDictionaryModelAdmin):
    """Admin model for the developer model."""

    inlines = (GameInline,)
    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields, "developer_logo_tag")
    list_display = (*BaseDictionaryModelAdmin.list_display, "developer_logo_tag")
