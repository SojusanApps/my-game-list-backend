from django.contrib import admin

from my_game_list.games.models import (
    Developer,
    Game,
    GameFollow,
    GameList,
    GameReview,
    Genre,
    Platform,
    Publisher,
)
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


class GameInline(admin.StackedInline):
    raw_id_fields = ("publisher",)
    extra = 0
    model = Game


@admin.register(Publisher)
class PublisherAdmin(BaseDictionaryModelAdmin):
    inlines = (GameInline,)


@admin.register(Developer)
class DeveloperAdmin(BaseDictionaryModelAdmin):
    inlines = (GameInline,)


@admin.register(Genre)
class GenreAdmin(BaseDictionaryModelAdmin):
    pass


@admin.register(Platform)
class PlatformAdmin(BaseDictionaryModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = readonly_fields + (
        "title",
        "publisher__name",
        "developer__name",
        "genres__name",
        "platforms__name",
    )
    raw_id_fields = ("publisher", "developer")
    list_filter = ("creation_time", "last_modified", "release_date")
    list_display = readonly_fields + list_filter + raw_id_fields + ("title", "cover_image")


@admin.register(GameList)
class GameListAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = readonly_fields + ("game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("status", "creation_time", "last_modified")
    list_display = readonly_fields + list_filter + raw_id_fields


@admin.register(GameFollow)
class GameFollowAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = readonly_fields + ("game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("creation_time",)
    list_display = readonly_fields + list_filter + raw_id_fields


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = readonly_fields + ("game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = (
        "score",
        "creation_time",
    )
    list_display = readonly_fields + list_filter + raw_id_fields
