from django.conf import settings
from ks_settings.settings import enable_when, l
from django.urls import include, path


def get_urls() -> list:
    return l(path("api-auth/", include("rest_framework.urls")))