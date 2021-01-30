"""Django settings for foodgram project."""

import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY", default=get_random_secret_key())

DEBUG = bool(int(os.environ.get("DEBUG") if os.environ.get("DEBUG") else "0"))

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    "food-gram.cf",
]


INSTALLED_APPS = [
    "users",
    "recipes.apps.RecipesConfig",
    "api",
    "about",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "debug_toolbar",  # for django-debug-toolbar
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # for django-debug-toolbar
]

# for django-debug-toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "foodgram.urls"

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

WSGI_APPLICATION = "foodgram.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("DB_ENGINE"),
#         "NAME": os.environ.get("POSTGRES_DB"),
#         "USER": os.environ.get("POSTGRES_USER"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#         "HOST": os.environ.get("DB_HOST"),
#         "PORT": os.environ.get("DB_PORT"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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


LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "index"

#  подключаем движок filebased.EmailBackend
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# указываем директорию, в которую будут складываться файлы писем
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

AUTH_USER_MODEL = "users.RecipeUser"

SHOPLIST_SESSION_ID = "shoplist"
