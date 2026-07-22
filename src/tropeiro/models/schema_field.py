from django_pydantic_field.v2.fields import PydanticSchemaField
from django_pydantic_field.compat import GenericContainer
from pydantic import RootModel


class SchemaField(PydanticSchemaField):
    def __new__(cls, schema, **kw):
        self = super().__new__(cls)

        if not isinstance(schema, GenericContainer):
            schema = RootModel[schema]

        self.__init__(schema=schema, **kw)
        return self
