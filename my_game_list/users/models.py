from django.contrib.auth.models import AbstractUser

from my_game_list.my_game_list.models import BaseModel


class User(BaseModel, AbstractUser):
    pass
