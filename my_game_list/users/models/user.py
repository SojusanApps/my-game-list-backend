"""This module contains the User model."""
from typing import Self

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseModel


class User(BaseModel, AbstractUser):
    """A model for the application user."""

    # Delete the unwanted fields from the `AbstractUser`
    # first and last name of the user are sensitive data that will not be used in the application
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    avatar = models.BinaryField(_("avatar"), max_length=307200, blank=True, null=True, editable=True)

    def __str__(self: Self) -> str:
        """Return a string representation for this model."""
        return f"{self.username} - {self.email}"
