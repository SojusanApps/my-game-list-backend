from django.contrib import admin

from my_game_list.friendships.models import FriendList


@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = readonly_fields + ("user__username",)
    raw_id_fields = (
        "user",
        "friends",
    )
    list_display = readonly_fields + ("user",)
