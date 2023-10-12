import os
import uuid
from django.db import models
from users.models import User
from django.contrib.auth import get_user_model
import mimetypes
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.core.files.base import ContentFile
from bs4 import BeautifulSoup
import requests
import pypinyin


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
    name = models.CharField(max_length=40, unique=True)

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
        if self.image == "" or self.image is None:
            return "/media/static_default/{}.png".format(self.initial)
        else:
            return self.image.url

    @property
    def all_tags(self):
        if self.tags.all() == "" or self.tags.all() is None:
            return None
        else:
            return self.tags.all()
          
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
 
def get_room_image_upload_path(instance, filename):
    room_name = instance.room.name
    upload_path = os.path.join('room_files', room_name)
    file_path = os.path.join(upload_path, filename)
    media_upload_path = os.path.join('media', upload_path)
    if not os.path.exists(media_upload_path):
        os.makedirs(media_upload_path)
    return file_path


def get_friend_files_path(instance, filename):
    uid = instance.belong_fm.uid
    upload_path = os.path.join('friends_files', str(uid))
    file_path = os.path.join(upload_path, filename)
    media_upload_path = os.path.join('media', upload_path)
    if not os.path.exists(media_upload_path):
        os.makedirs(media_upload_path)
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
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    belong_post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to=get_room_image_upload_path, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
    def save(self, *args, **kwargs):
        if self.attachment.name:
            validate_file_size(self.attachment)
        super().save(*args, **kwargs)
        
    @property
    def image_url(self):
        profile = Profile.objects.get(user=self.user)
        return profile.image_url

    @property
    def attachment_url(self):
        if self.attachment.name == "" or self.attachment.name is None:
            return ""
        return self.attachment.url
    
    @property
    def attachment_type(self):
        file_type, _ = mimetypes.guess_type(self.attachment.name)
        if file_type.startswith("image"):
            file_type = "image"
        return file_type
    
    @property
    def attachment_name(self):
        if self.attachment.name == "" or self.attachment.name is None:
            return None
        return os.path.basename(self.attachment.name)
        
    @property
    def attachment_size(self):
        try:
            size = os.path.getsize(self.attachment.path)
            return convert_size(size)
        except:
            return 'Unknown Size'
        

class Friend_Request(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    invite_message = models.CharField(max_length=50)
    
    @property
    def from_user_profile(self):
        return Profile.objects.get(user=self.from_user)
    
    @property
    def to_user_profile(self):
        return Profile.objects.get(user=self.to_user)
    

class FriendRoom(models.Model):
    """
    A flexible and freely accessible space
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendroom_user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendroom_user_2')
    
    def __str__(self):
        return f'FR({self.user_1.username}, {self.user_2.username})'
    

class FMMessage(models.Model):
    """
    Message for FriendRoom
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    belong_fm = models.ForeignKey(to=FriendRoom, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to=get_friend_files_path, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
    def save(self, *args, **kwargs):
        if self.attachment.name:
            validate_file_size(self.attachment)
        super().save(*args, **kwargs)
       
    @property
    def image_url(self):
        profile = Profile.objects.get(user=self.user)
        return profile.image_url

    @property
    def attachment_url(self):
        if self.attachment.name == "" or self.attachment.name is None:
            return ""
        return self.attachment.url
    
    @property
    def attachment_type(self):
        file_type, _ = mimetypes.guess_type(self.attachment.name)
        if file_type.startswith("image"):
            file_type = "image"
        return file_type
    
    @property
    def attachment_name(self):
        if self.attachment.name == "" or self.attachment.name is None:
            return None
        return os.path.basename(self.attachment.name)
        
    @property
    def attachment_size(self):
        try:
            size = os.path.getsize(self.attachment.path)
            return convert_size(size)
        except:
            return 'Unknown Size'
        
def get_first_pinyin_letter(chinese):
    pinyin = pypinyin.pinyin(chinese[0], style=pypinyin.STYLE_NORMAL)[0][0]
    return pinyin[0].upper()

class LINK(models.Model):
    url = models.URLField(
        max_length=100, help_text="Enter a link of a website", unique=True
    )
    name = models.CharField(max_length=100, help_text="Enter the name of a website")
    user = models.ManyToManyField(User)
    image = models.ImageField(upload_to="link_image", null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.url

    @property
    def initial(self):
        if pypinyin.pinyin(self.name[0]):
            return get_first_pinyin_letter(self.name[0]).upper()
        return self.name[0].upper()

    @property
    def image_url(self):
        if self.image == "":
            # return "/media/static_default/{}.png".format(self.initial)
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/30.0.1599.17 Safari/537.36"
                )
            }  # 伪装请求头
            try:
                response = requests.get(self.url, headers=headers, timeout=1)
            except:
                return "/media/static_default/{}.png".format(self.initial)
            soup = BeautifulSoup(response.text, "html.parser")
            favicon = soup.find(
                "link", href=True,  rel=lambda x: x and "icon" in x
            )
            # favicon = favicon[0] if favicon else None
            if favicon:
                favicon = favicon["href"]
            else:
                return "/media/static_default/{}.png".format(self.initial)
            if favicon.startswith("//"):
                favicon = "https:" + favicon
            elif favicon.startswith("/"):
                favicon = self.url + favicon
            if favicon:
                favicon_resp = requests.get(favicon, headers=headers)
                domain = self.url.split("//")[-1].split(".")[1]
                path = "media/link_image/"
                fullpath = path + domain + ".png"
                name = domain + ".png"
                self.image.save(name, ContentFile(favicon_resp.content))
            else:
                return "/media/static_default/{}.png".format(self.initial)
        return self.image.url
