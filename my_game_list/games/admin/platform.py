from django.contrib import admin

from my_game_list.games.models import Platform
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Platform)
class PlatformAdmin(BaseDictionaryModelAdmin):
    pass