from django.contrib import admin

from my_game_list.games.models import GameReview


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
