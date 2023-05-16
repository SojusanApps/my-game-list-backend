# ruff: noqa
from my_game_list.settings.base import *

DEBUG = oeg("DJANGO_DEBUG", "True").lower() == "true"

INSTALLED_APPS += [
    "rosetta",
]

CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "rest_framework.authentication.BasicAuthentication",
    "rest_framework_simplejwt.authentication.JWTAuthentication",
)

STATIC_URL = "/static/"
STATIC_ROOT = f"/{BASE_DIR.parent}/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = f"/{BASE_DIR.parent}/media/"
