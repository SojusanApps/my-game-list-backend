from my_game_list.settings.base import *  # noqa

DEBUG = oeg("DJANGO_DEBUG", "True").lower() == "true"

INSTALLED_APPS += [
    "rosetta",
]

STATIC_URL = "/static/"
STATIC_ROOT = f"/{BASE_DIR.parent}/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = f"/{BASE_DIR.parent}/media/"
