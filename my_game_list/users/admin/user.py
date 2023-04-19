from django.contrib import admin

from my_game_list.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin model for the User model."""

    readonly_fields = ("id",)
    search_fields = ("id", "username", "email")
    list_filter = ("is_superuser", "is_staff", "is_active", "date_joined")
    list_display = search_fields + list_filter + ("last_login", "avatar")
