from rest_framework.serializers import BaseSerializer
from types import NoneType
from rest_framework.fields import UUIDField
from tropeiro.serializers.schema_field import SchemaField
from django_pydantic_field.fields import PydanticSchemaField
from tropeiro.models import Model
from typing import cast, Literal, Callable, Any
from rest_framework import serializers


class HashidField(serializers.SlugRelatedField):
    def __init__(self, **kwargs) -> None:
        slug_field = "id"
        if (queryset := kwargs.get("queryset", None)) is not None and hasattr(
            queryset.model, "uuid"
        ):
            slug_field = "uuid"

        super().__init__(slug_field, **kwargs)


class ModelSerializerMeta(type(serializers.ModelSerializer)):
    def __new__(cls, name, bases, namespace):
        """DRF throws an error if a parent class defines a field but
        the child class excludes it.

        This metaclass sets all of `Meta.exclude` attributes to None as a fix.
        """
        for k in namespace["Meta"].exclude or []:
            namespace[k] = None

        return super().__new__(cls, name, bases, namespace)


class ModelSerializer(serializers.ModelSerializer, metaclass=ModelSerializerMeta):
    def __getattr__(self, name: str, /):
        """implements looking up the instantiated field"""
        if name in self.fields:
            return self.fields[name]
        return super().__getattribute__(name)

    serializer_related_field = HashidField
    uuid = UUIDField(read_only=True)

    class Meta:
        model: type[Model]
        fields = None
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
            if hasattr(cls, "fields") and cls.fields is not None:
                cls.exclude = None
            elif (
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
    fields: list[str] | Literal["__all__"] | None = None,
) -> type[ModelSerializer]:
    name = name or f"{model_cls.__name__}Serializer"
    exclude_ = exclude
    fields_ = fields
    assert isinstance(exclude_, (NoneType, list))
    assert isinstance(fields_, (NoneType, list, str))

    if isinstance(fields_, list):
        assert not exclude
        fields_ += list(extra_fields.keys())

    class InnerSerializer(ModelSerializer):
        locals().update(extra_fields)

        class Meta(ModelSerializer.Meta):
            model = model_cls
            exclude = exclude_
            fields = fields_

    InnerSerializer.__name__ = name
    InnerSerializer.__qualname__ = f"{name}"

    return InnerSerializer


class SerializerFunctionField[M: Model](serializers.Field):
    def __init__(self, method: Callable[[M], Any], **kwargs):
        self.method = method
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        return self.method(value)


__all__ = ["SerializerFunctionField", "SimpleSerializer", "ModelSerializer"]
