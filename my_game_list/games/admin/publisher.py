from django.contrib import admin

from my_game_list.games.admin.game import GameInline
from my_game_list.games.models import Publisher
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Publisher)
class PublisherAdmin(BaseDictionaryModelAdmin):
    inlines = (GameInline,)
