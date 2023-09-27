from django.db import models
from users.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

class Profile(models.Model):
    """
    Personal Profile
    """
    about_me = models.TextField(default='There is no Personal Signature here yet. You can add it through settings')
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, default="Unkown")
    
    @property
    def image_url(self):
        if self.image == "":
            return "/media/chat/static_default/{}.png".format(self.user_initial)
        else:
            return self.image.url
        
    @property
    def user_initial(self):
        return self.user.username[0].upper()
    
    def __str__(self):
        return self.user.username
    
    
class Room(models.Model):
    """
    A flexible and freely accessible space
    """
    name = models.CharField(max_length=128, unique=True)
    owner_name = models.CharField(max_length=128)
    about_room = models.CharField(max_length=128, default="welcome to my chatroom")
    online = models.ManyToManyField(to=get_user_model(), blank=True)
    image = models.ImageField(upload_to='room_image', null=True, blank=True)
    
    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    @property
    def initial(self):
        return self.name[0].upper()
    
    @property
    def image_url(self):
        if self.image == "":
            return "/media/chat/static_default/{}.png".format(self.initial)
        else:
            return self.image.url
    
    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class RoomMessage(models.Model):
    """
    Message for Room
    """
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'

    @property
    def image_url(self):
        profile = Profile.objects.get(user=self.user)
        return profile.image_url