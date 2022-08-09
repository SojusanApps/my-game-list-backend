from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseModel
from my_game_list.my_game_list.validators import validate_file_size


class Gender(models.TextChoices):
    """The gender of the user."""

    MALE = "M", _("Male")
    FEMALE = "F", _("Female")


class User(BaseModel, AbstractUser):
    """A model for the application user."""

    avatar = models.ImageField(
        _("avatar"), upload_to="avatars/", blank=True, null=True, validators=[validate_file_size]
    )
    gender = models.CharField(_("gender"), max_length=1, choices=Gender.choices)
