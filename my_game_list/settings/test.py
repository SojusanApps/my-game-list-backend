# ruff: noqa
import os

os.environ["DJANGO_CORS_ALLOWED_ORIGINS"] = "http://test"
from my_game_list.settings.base import *

DEBUG = oeg("DJANGO_DEBUG", "False").lower() == "true"

DATABASES = {
    "default": {
        "ENGINE": oeg("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": oeg("POSTGRES_DB", "pytest_postgresql"),
        "USER": oeg("POSTGRES_USER", "pytest_postgresql"),
        "PASSWORD": oeg("POSTGRES_PASSWORD", "pytest_postgresql"),
        "HOST": oeg("POSTGRES_HOST", "localhost"),
        "PORT": oeg("POSTGRES_PORT", "9999"),
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = f"/tmp/my-game-list/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = f"/tmp/my-game-list/media/"
