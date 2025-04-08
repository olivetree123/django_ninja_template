import uuid

from django.db import models
from django.utils import timezone


def get_uuid():
    return uuid.uuid4().hex


class BaseModel(models.Model):
    uid = models.CharField(max_length=32, default=get_uuid, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @classmethod
    async def aget_by_uid(cls, uid):
        return await cls.objects.filter(uid=uid, is_deleted=False).afirst()

    @classmethod
    def get_by_uid(cls, uid):
        return cls.objects.filter(uid=uid, is_deleted=False).first()
