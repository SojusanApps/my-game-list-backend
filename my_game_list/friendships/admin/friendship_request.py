"""This module contains the admin model for the FriendshipRequest model."""

from django.contrib import admin

from my_game_list.friendships.models import FriendshipRequest


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin[FriendshipRequest]):
    """Admin model for the friendship request model."""

    readonly_fields = ("id",)
    search_fields = (*readonly_fields, "sender__username", "receiver__username")
    raw_id_fields = ("sender", "receiver")
    list_filter = ("created_at", "last_modified_at", "rejected_at")
    list_display = (*readonly_fields, *list_filter, *raw_id_fields)
