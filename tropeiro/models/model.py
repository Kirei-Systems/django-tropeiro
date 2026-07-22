from django.conf import settings
import datetime
from uuid import UUID
from django.db import models
from uuid_extensions import uuid7

User = settings.AUTH_USER_MODEL


def uuid() -> UUID:
    a = uuid7()
    assert isinstance(a, UUID)
    return a


class Model(models.Model):
    uuid = models.UUIDField(default=uuid, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        related_name="created_%(model_name)s",
    )
    active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(
        null=True,
        editable=False,
    )
    deleted_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        default=None,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="deleted_%(model_name)s",
    )

    def delete(self, deleted_by: "User", *a, for_real=False, **kw):
        if for_real:
            super().delete(*a, **kw)
        else:
            self.active = False
            self.deleted_at = datetime.datetime.now()
            self.deleted_by = deleted_by

    class Meta:
        abstract = True
