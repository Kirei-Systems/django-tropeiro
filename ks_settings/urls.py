from ks_settings.settings import enable_when, enable_list_when, l, SETTINGS
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin


def get_urls() -> list:
    urlpatterns = l(
        enable_when(
            SETTINGS.django_rest_framework,
            lambda: path("api-auth/", include("rest_framework.urls")),
        ),
        *enable_list_when(
            settings.DEBUG,
            lambda: static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        ),
    ) + i18n_patterns(
        path("admin/", admin.site.urls),
        # If no prefix is given, use the default language
        prefix_default_language=False,
    )

    return urlpatterns
