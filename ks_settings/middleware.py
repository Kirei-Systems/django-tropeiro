from typing import Any
from django.utils.cache import add_never_cache_headers


class DisableCacheMiddleware:
    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response
        pass

    def __call__(self, request: Any):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response
