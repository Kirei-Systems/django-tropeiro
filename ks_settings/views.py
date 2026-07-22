from ks_settings.serializers import ModelSerializer
from django.core.exceptions import ImproperlyConfigured
import sys
from ks_settings.models import Model, AbstractUser
from django.db.models import Model as DjangoModel
from rest_framework.serializers import Serializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 1000


class AbstractViewSetMixin[U: AbstractUser](viewsets.GenericViewSet):
    user_class: type[U]
    pagination_class = StandardResultsSetPagination
    lookup_field = "uuid"

    read_serializer_class: type[Serializer] | None = None
    write_serializer_class: type[Serializer] | None = None

    @property
    def model(self) -> type[DjangoModel]:
        cls = self.get_serializer_class()
        assert issubclass(cls, ModelSerializer)
        return cls.Meta.model

    def get_serializer_class(self) -> type[Serializer]:
        try:
            super().get_serializer_class()
        except Exception as e:
            print(e, file=sys.stderr)
        if self.action in ["create", "update", "partial_update"]:
            return self.write_serializer_class or super().get_serializer_class()
        else:
            return self.read_serializer_class or super().get_serializer_class()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # drf-spectacular
            return self.model.objects.none()

        return self.model.objects.filter(
            active=True,
        )

    @property
    def user(self) -> U:
        assert isinstance(self.request.user, self.user_class)
        return self.request.user

    def perform_destroy(self, instance: DjangoModel) -> None:
        if isinstance(instance, Model):
            instance.delete(deleted_by=self.user)
        else:
            instance.delete()

    def perform_create(self, serializer):
        if issubclass(self.model, Model):
            serializer.save(created_by=self.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if issubclass(self.model, Model):
            serializer.save(created_by=self.user)
        else:
            serializer.save()

    def __init_subclass__(cls):
        name = f"`{cls.__name__}`"
        if hasattr(cls, "serializer"):
            raise ImproperlyConfigured(
                f"Found field `serializer` in class {name}. Did you mean `serializer_class`?"
            )
        if all(
            [
                not hasattr(cls, attr)
                for attr in [
                    "serializer_class",
                    "read_serializer_class",
                    "write_serializer_class",
                ]
            ]
        ):
            raise ImproperlyConfigured(
                f"No serializer found for class {name}. Start by defining `serializer_class`"
            )


class AbstractModelViewSet[U: AbstractUser](
    AbstractViewSetMixin[U], viewsets.ModelViewSet
):
    pass
