"""This module contains the User model."""
from base64 import b64encode
from typing import ClassVar, Self

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseModel


class User(BaseModel, AbstractUser):
    """A model for the application user."""

    email = models.EmailField(_("email address"), unique=True)

    # Delete the unwanted fields from the `AbstractUser`
    # first and last name of the user are sensitive data that will not be used in the application
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    avatar = models.BinaryField(_("avatar"), max_length=307200, blank=True, null=True, editable=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["username"]

    def __str__(self: Self) -> str:
        """Return a string representation for this model."""
        return f"{self.username} - {self.email}"

    @property
    @admin.display(description="Avatar preview")
    def avatar_tag(self: Self) -> str:
        """Used in admin model to have a image preview."""
        if self.avatar:
            return format_html(
                '<img src = "data: image/png; base64, {}" width="125" height="150">',
                b64encode(self.avatar).decode("utf-8"),
            )
        return ""
