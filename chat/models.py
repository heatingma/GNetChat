import os
from django.db import models
from users.models import User
from django.contrib.auth import get_user_model
import mimetypes
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


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
            return "/media/static_default/{}.png".format(self.user_initial)
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
            return "/media/static_default/{}.png".format(self.initial)
        else:
            return self.image.url
    
    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'

class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
  

class Post(models.Model):
    """
    A flexible and freely accessible space
    """
    title = models.CharField(max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    author_profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    about_post = models.CharField(max_length=1000, default="The author did not set an introduction to the topic")
    image = models.ImageField(upload_to='post_image', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    belong_room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def initial(self):
        return self.title[0].upper()
    
    class Meta:
        ordering = ['-created_on']
        
    @property
    def image_url(self):
        if self.image == "":
            return "/media/static_default/{}.png".format(self.initial)
        else:
            return self.image.url
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
 
def get_room_image_upload_path(instance, filename):
    room_name = instance.room.name
    upload_path = os.path.join('room_files', room_name)
    file_path = os.path.join(upload_path, filename)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    return file_path


def convert_size(size):
    KB = 1024
    MB = KB ** 2
    GB = KB ** 3

    if size < KB:
        return f"{size} B"
    elif size < MB:
        return f"{size / KB:.2f} KB"
    elif size < GB:
        return f"{size / MB:.2f} MB"
    else:
        return f"{size / GB:.2f} GB"
    

def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("File size cannot exceed 5MB.")
 
 
class RoomMessage(models.Model):
    """
    Message for Room
    """
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    belong_post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to=get_room_image_upload_path, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
    def save(self):
        validate_file_size(self.attachment)
        super().save()
        
    @property
    def image_url(self):
        profile = Profile.objects.get(user=self.user)
        return profile.image_url

    @property
    def attachment_type(self):
        file_type, _ = mimetypes.guess_type(self.attachment.name)
        if file_type.startswith("image"):
            file_type = "image"
        return file_type
    
    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name)

    @property
    def attachment_size(self):
        size = os.path.getsize(self.attachment.path)
        return convert_size(size)
    