from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField('email address', primary_key=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]