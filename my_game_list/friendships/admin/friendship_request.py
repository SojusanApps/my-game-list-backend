from django.contrib import admin

from my_game_list.friendships.models import FriendshipRequest


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = readonly_fields + ("sender__username", "receiver__username")
    raw_id_fields = ("sender", "receiver")
    list_filter = ("is_active", "creation_time", "last_modified")
    list_display = readonly_fields + list_filter + raw_id_fields
