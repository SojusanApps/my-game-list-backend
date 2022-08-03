import os

os.environ["DJANGO_CORS_ALLOWED_ORIGINS"] = "http://test"
from my_game_list.settings.base import *  # noqa

DEBUG = oeg("DJANGO_DEBUG", "False").lower() == "true"

DATABASES = {
    "default": {
        "ENGINE": oeg("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": oeg("POSTGRES_DB", "my_game_list"),
        "USER": oeg("POSTGRES_USER", "my_game_list"),
        "PASSWORD": oeg("POSTGRES_PASSWORD", "my_game_list"),
        "HOST": oeg("POSTGRES_HOST", "localhost"),
        "PORT": oeg("POSTGRES_PORT", "5432"),
    }
}
