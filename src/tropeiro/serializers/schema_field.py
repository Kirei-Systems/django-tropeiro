from pydantic import RootModel
from rest_framework.fields import ModelField
from drf_spectacular.drainage import set_override


class SchemaField(ModelField):
    def __init__(self, **kw):
        print(kw)
        schema = kw["model_field"].schema

        set_override(self, "field", RootModel[schema])
        for k in ["encoder", "decoder"]:
            kw.pop(k)
        super().__init__(**kw)
