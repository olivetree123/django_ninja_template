from django.db import models

from main.models.base import BaseModel


class User(BaseModel):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = "user"
