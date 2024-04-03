"""This module contains the admin model for the User model."""
from typing import Any, ClassVar

from django.contrib import admin
from django.db import models

from my_game_list.my_game_list.forms import BinaryFieldWithUpload
from my_game_list.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
    """Admin model for the User model."""

    formfield_overrides: ClassVar[dict[type[models.Field[Any, Any]], dict[str, Any]]] = {  # type: ignore[misc]
        models.BinaryField: {
            "form_class": BinaryFieldWithUpload,
        },
    }
    readonly_fields = ("id", "avatar_tag")
    search_fields = ("id", "username", "email")
    list_filter = ("is_superuser", "is_staff", "is_active", "date_joined")
    list_display = (*search_fields, *list_filter, "gender", "last_login", "avatar", "avatar_tag")
