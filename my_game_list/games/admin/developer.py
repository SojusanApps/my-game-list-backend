from django.contrib import admin

from my_game_list.games.admin.game import GameInline
from my_game_list.games.models import Developer
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Developer)
class DeveloperAdmin(BaseDictionaryModelAdmin):
    """Admin model for the developer model."""

    inlines = (GameInline,)
