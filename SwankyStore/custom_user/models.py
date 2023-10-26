from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager

class User(BaseUser):
    username = models.CharField(max_length=30, unique=True)
    objects = BaseUserManager()
