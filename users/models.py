from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import *


class BaseModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ProfileManager()

    def __str__(self):
        return self.email
