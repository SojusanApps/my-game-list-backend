import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

oeg = os.environ.get

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = oeg("DJANGO_SECRET_KEY", "secret_key_to_change_on_production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = oeg("DJANGO_DEBUG", "False").lower() == "true"

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
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_extensions",
    "django_filters",
    "corsheaders",
    # Internal apps
    f"{MAIN_APP}.{MAIN_APP}",
    f"{MAIN_APP}.users",
    f"{MAIN_APP}.games",
    f"{MAIN_APP}.friendships",
    # This one must be the last to ensure that exceptions inside other app's
    # signal handlers do not affect the integrity of file deletions within transactions
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
    }
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
    os.path.join(BASE_DIR, "locale"),
]

STATIC_URL = "/static/"
STATIC_ROOT = f"/opt/{MAIN_APP}/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = f"/opt/{MAIN_APP}/media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

CORS_ALLOWED_ORIGINS = oeg("DJANGO_CORS_ALLOWED_ORIGINS", "http://localhost:4200").split(",")

LIMIT_AVATAR_SIZE = int(oeg("MGL_LIMIT_AVATAR_SIZE", 200 * 1024))  # 200 KiB
