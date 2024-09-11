"""This module contains the User model."""

import hashlib
from typing import ClassVar, Self

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseModel


class Gender(models.TextChoices):
    """The choices for the gender of the user."""

    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    PREFER_NOT_TO_SAY = "X", _("Prefer not to say")


class User(BaseModel, AbstractUser):
    """A model for the application user."""

    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(_("gender"), max_length=1, choices=Gender.choices, default=Gender.PREFER_NOT_TO_SAY)

    # Delete the unwanted fields from the `AbstractUser`
    # first and last name of the user are sensitive data that will not be used in the application
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["username"]

    def __str__(self: Self) -> str:
        """Return a string representation for this model."""
        return f"{self.username} - {self.email}"

    @property
    def gravatar_url(self: Self) -> str:
        """Generate the gravatar url for the user."""
        email_hash = hashlib.sha256(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s=256"

    @property
    @admin.display(description="Gravatar preview")
    def gravatar_tag(self: Self) -> str:
        """Used in admin model to have a image preview."""
        return format_html(
            '<img src={} width="125" height="150">',
            self.gravatar_url,
        )
