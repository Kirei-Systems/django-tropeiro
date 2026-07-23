from django_pydantic_field.v2.fields import PydanticSchemaField
from django_pydantic_field.compat import GenericContainer


class SchemaField(PydanticSchemaField):
    def __new__(cls, schema, **kw):
        self = super().__new__(cls)

        if isinstance(schema, GenericContainer):
            schema = schema.origin[*schema.args]

        self.__init__(schema=schema, **kw)
        return self
