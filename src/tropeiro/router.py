from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter


class Router:
    def __init__(self):
        self.router = DefaultRouter()

    def register(self, route: str, name: str | None = None):
        route = route.removeprefix("/")
        name = name or route

        def inner(cls):
            self.router.register(route, cls, name)
            return cls

        return inner

    def include(self, prefix: str = ""):
        return path(prefix, include(self.router.urls))
