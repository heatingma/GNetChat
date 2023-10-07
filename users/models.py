from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    top_friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends_set')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='top_friends_set')
    email = models.EmailField('email address', primary_key=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    @property
    def image_url(self):
        from chat.models import Profile
        return Profile.objects.get(user=self).image_url
    
    @property
    def about_me(self):
        from chat.models import Profile
        return Profile.objects.get(user=self).about_me
    