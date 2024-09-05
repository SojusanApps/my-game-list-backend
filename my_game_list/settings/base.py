"""This is a base configuration for MyGameList Django application."""

import os
from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from my_game_list import __version__

oeg = os.environ.get

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = oeg("DJANGO_SECRET_KEY", "secret_key_to_change_on_production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = oeg("DJANGO_DEBUG", "False").lower() == "true"

CORS_ALLOWED_ORIGINS = oeg("DJANGO_CORS_ALLOWED_ORIGINS", "*").split(",")
ALLOWED_HOSTS = oeg("DJANGO_ALLOWED_HOSTS", "*").split(",")

DOCUMENTATION_ENABLED = oeg("DJANGO_DOCUMENTATION_ENABLED", "True").lower() == "true"

MAIN_APP = "my_game_list"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_extensions",
    "django_filters",
    "corsheaders",
    "django_prometheus",
    # Internal apps
    f"{MAIN_APP}.{MAIN_APP}",
    f"{MAIN_APP}.users",
    f"{MAIN_APP}.games",
    f"{MAIN_APP}.friendships",
    # This must be the last to ensure that exceptions inside other app's
    # signal handlers do not affect the integrity of file deletions within transactions
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = f"{MAIN_APP}.{MAIN_APP}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = f"{MAIN_APP}.{MAIN_APP}.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": oeg("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": oeg("POSTGRES_DB", "my_game_list"),
        "USER": oeg("POSTGRES_USER", "my_game_list"),
        "PASSWORD": oeg("POSTGRES_PASSWORD", "my_game_list"),
        "HOST": oeg("POSTGRES_HOST", "localhost"),
        "PORT": oeg("POSTGRES_PORT", "5432"),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGES = (
    ("pl", _("Polish")),
    ("en", _("English")),
)

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = "en"
ROSETTA_SHOW_AT_ADMIN_PANEL = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

STATIC_URL = "/static/"
STATIC_ROOT = f"/opt/{MAIN_APP}/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = f"/opt/{MAIN_APP}/media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

CORS_ALLOWED_ORIGINS = oeg("DJANGO_CORS_ALLOWED_ORIGINS", "http://localhost:4200").split(",")

LIMIT_FILE_SIZE = int(os.environ.get("MGL_LIMIT_FILE_SIZE", 200 * 1024))  # 200 KiB

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PERMISSION_CLASSES": "rest_framework.permissions.IsAuthenticated",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "MyGameList API",
    "DESCRIPTION": "Application to manage game lists.",
    "VERSION": ".".join(map(str, __version__)),
    "SCHEMA_PATH_PREFIX": "/api/",
}

MGL_LOG_DIR_PATH = oeg("MGL_LOG_DIR_PATH", BASE_DIR.parent / "logs")
MGL_LOG_FILENAME = oeg("MGL_LOG_FILENAME", "my_game_list.log")

if not (log_path := Path(MGL_LOG_DIR_PATH)).is_dir():
    log_path.mkdir(exist_ok=True)

LOG_FILE_PATH = Path(MGL_LOG_DIR_PATH, MGL_LOG_FILENAME)
LOGLEVEL = oeg("DJANGO_LOGLEVEL", "INFO").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "{log_color}[{asctime}] {levelname}\t{module} - {funcName} :: {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "light_black",
                "INFO": "cyan",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "colorlog.StreamHandler",
            "formatter": "color",
            "filters": ["require_debug_true"],
        },
        "file": {
            "level": LOGLEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "color",
            "backupCount": 5,
            "maxBytes": 5242880,  # 5*1024*1024 bytes (5MB)
            "filename": LOG_FILE_PATH,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "error": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "django": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "django.server": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

MYPYPATH = BASE_DIR / "stubs"
