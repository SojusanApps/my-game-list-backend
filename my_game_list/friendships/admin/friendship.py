"""This module contains the admin model for the Friendship model."""
from django.contrib import admin

from my_game_list.friendships.models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    """Admin model for the friendship model."""

    readonly_fields = ("id", "created_at")
    search_fields = (*readonly_fields, "user__username")
    raw_id_fields = (
        "user",
        "friend",
    )
    list_display = (*readonly_fields, *raw_id_fields)
