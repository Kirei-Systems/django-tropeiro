from collections.abc import Callable
from dataclasses import dataclass
import os
from tropeiro import env


def l(*args) -> list:
    return [a for a in args if a is not None]


def d(val: dict) -> dict:
    return {k: v for k, v in val.items() if v is not None}


def enable_when[T](flag: bool, val: T | Callable[[], T]) -> None | T:
    if flag:
        if callable(val):
            return val()
        else:
            return val


def enable_list_when[T](flag: bool, val: list[T] | Callable[[], list[T]]) -> list[T]:
    if flag:
        if callable(val):
            return val()
        else:
            return val
    return []


def settings(
    settings_locals: dict,
    *,
    time_zone="America/Sao_Paulo",
    langcode="pt-br",
    apps: list[str],
    disable_cache: bool = True,
    pre_middleware: list[str] = [],
    middleware: list[str] = [],
    staticfiles_dirs: list[str] = ["public"],
):

    PROJECT_NAME = env.project_name()
    PROJECT_SLUG = PROJECT_NAME.replace("_", "-")
    BASE_DIR = env.project_dir()
    DEBUG = os.environ.get("PRODUCTION", "") != "true"
    HOSTS = l(os.environ.get("HOST"))
    ALLOWED_HOSTS = l(enable_when(DEBUG, "*"), *HOSTS)
    CSRF_TRUSTED_ORIGINS = ["https://" + host for host in HOSTS]

    if not DEBUG and len(ALLOWED_HOSTS) == 0:
        raise Exception("Empty HOSTS env var in a production environment")

    MEDIA_URL = "media/"
    if DEBUG:
        MEDIA_ROOT = "media/"
    else:
        MEDIA_ROOT = f"/var/media/{PROJECT_SLUG}"

    SECRET_KEY = "django-insecure-=f^dje6)gpg@y3!mt4dmji-r(@ghfz"
    if not DEBUG:
        SECRET_KEY = os.environ["SECRET_KEY"]

    INSTALLED_APPS = (
        l(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "drf_spectacular",
            "drf_spectacular_sidecar",
            "rest_framework",
        )
        + apps
    )

    MIDDLEWARE = (
        pre_middleware
        + l(
            enable_when(disable_cache, "tropeiro.middleware.DisableCacheMiddleware"),
            "django.middleware.security.SecurityMiddleware",
            "django.middleware.locale.LocaleMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        )
        + middleware
    )
    ROOT_URLCONF = f"{PROJECT_NAME}.urls"
    TEMPLATES = l(
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
    )
    WSGI_APPLICATION = f"{PROJECT_NAME}.wsgi.application"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": {
            "rest_framework.authentication.SessionAuthentication",
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

    LANGUAGE_CODE = langcode
    TIME_ZONE = time_zone
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    STATIC_URL = "static/"
    STATICFILES_DIRS = [BASE_DIR / dir for dir in staticfiles_dirs]
    if not DEBUG:
        STATIC_ROOT = f"/var/static/{PROJECT_SLUG}"

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    REST_FRAMEWORK = {
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

    SPECTACULAR_SETTINGS = {
        "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
        "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
        "REDOC_DIST": "SIDECAR",
        # OTHER SETTINGS
    }

    settings_locals.update(locals())
