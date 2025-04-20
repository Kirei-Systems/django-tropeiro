from typing import Any
from django.utils.cache import add_never_cache_headers
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse


class DisableCacheMiddleware:
    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response
        pass

    def __call__(self, request: Any):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response


class LoginRequiredMiddleware:
    """
    Middleware to ensure that all views require authentication,
    except for those explicitly allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.login_paths = getattr(settings, "LOGIN_URLS", [])

    def get_login_for_app(self, app: str) -> str:
        if login := self.login_paths.get(app, None):
            return login
        else:
            return self.login_paths["budgets"]

    def __call__(self, request):
        # If the user is not authenticated and the path is not excluded, redirect to login
        path = request.path
        if not request.user.is_authenticated and not self.is_exempt_path(path):
            app = path.split("/")[1]
            login_url = self.get_login_for_app(app)
            return redirect(f"{login_url}?next={request.path}", status=303)
        return self.get_response(request)

    def is_exempt_path(self, path):
        """
        Define which paths are exempt from authentication.
        """
        # Add additional public paths or static/media paths here
        return (
            path in self.login_paths.values()
            or path.startswith(settings.STATIC_URL)
            or path.startswith(settings.MEDIA_URL)
            or path.startswith("/__reload__")
        )
