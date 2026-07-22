from tropeiro.serializers.schema_field import SchemaField
from django_pydantic_field.fields import PydanticSchemaField
from tropeiro.models import Model
from typing import cast
from rest_framework import serializers


class HashidField(serializers.SlugRelatedField):
    def __init__(self, **kwargs) -> None:
        slug_field = "id"
        if (queryset := kwargs.get("queryset", None)) is not None and hasattr(
            queryset.model, "uuid"
        ):
            slug_field = "uuid"
        super().__init__(slug_field, **kwargs)


class ModelSerializer(serializers.ModelSerializer):
    def __getattr__(self, name: str, /):
        """implements looking up the instantiated field"""
        if name in self.fields:
            return self.fields[name]
        return super().__getattribute__(name)

    serializer_related_field = HashidField

    class Meta:
        model: type[Model]
        exclude: list | None = [
            "active",
            "deleted_at",
            "deleted_by",
            "created_at",
            "created_by",
            "updated_at",
        ]

        @classmethod
        def __init_subclass__(cls) -> None:
            if hasattr(cls, "fields"):
                cls.exclude = None
            if (
                cls.exclude is not ModelSerializer.Meta.exclude
                and cls.exclude is not None
            ):
                cls.exclude = (
                    cast(list[str], ModelSerializer.Meta.exclude) + cls.exclude
                )


ModelSerializer.serializer_field_mapping[PydanticSchemaField] = SchemaField  # type: ignore


def SimpleSerializer(
    model_cls: type[Model],
    name: str | None = None,
    extra_fields: dict[str, serializers.Field] = {},
    exclude=[],
) -> type[ModelSerializer]:
    name = name or f"{model_cls.__name__}Serializer"
    exclude_ = exclude

    class InnerSerializer(ModelSerializer):
        locals().update(extra_fields)

        class Meta(ModelSerializer.Meta):
            model = model_cls
            exclude = exclude_

    InnerSerializer.__name__ = name

    return InnerSerializer
