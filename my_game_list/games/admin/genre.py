from django.contrib import admin

from my_game_list.games.models import Genre
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Genre)
class GenreAdmin(BaseDictionaryModelAdmin):
    """Admin model for the genre model."""
