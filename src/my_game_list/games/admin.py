"""This module contains the admin models for game related data."""

from django.contrib import admin

from my_game_list.games.models import (
    Company,
    Game,
    GameFollow,
    GameList,
    GameMedia,
    GameReview,
    Genre,
    Platform,
)
from my_game_list.my_game_list.admin import BaseDictionaryModelAdmin


@admin.register(Company)
class CompanyAdmin(BaseDictionaryModelAdmin):
    """Admin model for the company model."""

    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields, "company_logo_tag")
    list_display = (*BaseDictionaryModelAdmin.list_display, "company_logo_tag")


@admin.register(GameFollow)
class GameFollowAdmin(admin.ModelAdmin[GameFollow]):
    """Admin model for the game follow model."""

    readonly_fields = ("id",)
    search_fields = (*readonly_fields, "game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("created_at",)
    list_display = (*readonly_fields, *list_filter, *raw_id_fields)


@admin.register(GameList)
class GameListAdmin(admin.ModelAdmin[GameList]):
    """Admin model for the game list model."""

    readonly_fields = ("id",)
    search_fields = (*readonly_fields, "game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("status", "created_at", "last_modified_at", "score")
    list_display = (*readonly_fields, *list_filter, *raw_id_fields)


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin[GameReview]):
    """Admin model for the game review model."""

    readonly_fields = ("id",)
    search_fields = (*readonly_fields, "game__title", "user__username")
    raw_id_fields = ("game", "user")
    list_filter = ("created_at",)
    list_display = (*readonly_fields, *list_filter, *raw_id_fields)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin[Game]):
    """Admin model for the game model."""

    readonly_fields = ("id", "cover_image_tag", "cover_image_id", "igdb_id")
    search_fields = (
        "id",
        "title",
        "igdb_id",
        "publisher__name",
        "developer__name",
        "genres__name",
        "platforms__name",
    )
    raw_id_fields = ("publisher", "developer")
    list_filter = ("created_at", "last_modified_at", "release_date")
    list_display = (
        *readonly_fields,
        *list_filter,
        *raw_id_fields,
        "title",
        "cover_image_id",
    )


@admin.register(Genre)
class GenreAdmin(BaseDictionaryModelAdmin):
    """Admin model for the genre model."""

    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields, "igdb_id")
    list_display = (*BaseDictionaryModelAdmin.list_display, "igdb_id")


@admin.register(Platform)
class PlatformAdmin(BaseDictionaryModelAdmin):
    """Admin model for the platform model."""

    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields, "igdb_id")
    list_display = (*BaseDictionaryModelAdmin.list_display, "abbreviation", "igdb_id")


@admin.register(GameMedia)
class GameMediaAdmin(BaseDictionaryModelAdmin):
    """Admin model for the game media model."""

    readonly_fields = (*BaseDictionaryModelAdmin.readonly_fields,)
    list_display = (*BaseDictionaryModelAdmin.list_display,)
