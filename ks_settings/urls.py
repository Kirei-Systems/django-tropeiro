from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from ks_settings.settings import enable_list_when, l
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin


def get_urls() -> list:
    urlpatterns = l(
        path("api/auth/", include("rest_framework.urls")),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/docs/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
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
