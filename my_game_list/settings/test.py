# ruff: noqa
"""This a configuration of the Django application for test runner."""
import os

os.environ["DJANGO_CORS_ALLOWED_ORIGINS"] = "https://test"
from my_game_list.settings.base import *  # NOSONAR

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

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "rest_framework.authentication.BasicAuthentication",
    "rest_framework_simplejwt.authentication.JWTAuthentication",
)

# Speed up the password hashing in tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

STATIC_URL = "/static/"
STATIC_ROOT = "/tmp/my-game-list/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/tmp/my-game-list/media/"
