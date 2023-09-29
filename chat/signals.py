from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Profile, RoomMessage, Room, Post, Tag
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        
@receiver(post_save, sender=Room)
def create_rm_cp(sender, instance, created, **kwargs):
    if created:
        # create the default chatting_post
        author = User.objects.get(username=instance.owner_name)
        profile = get_object_or_404(Profile, user=author)
        post = Post.objects.create(
            title =  "chatting_" + instance.name,
            author = author, 
            author_profile = profile,
            about_post = "The special and default post for chatting",
            belong_room=instance, 
        )
        try:
            post.tags.add(get_object_or_404(Tag, name="default"))
            post.tags.add(get_object_or_404(Tag, name="chatting"))
        except:
            Tag.objects.create(name="default")
            Tag.objects.create(name="chatting")
            post.tags.add(get_object_or_404(Tag, name="default"))
            post.tags.add(get_object_or_404(Tag, name="chatting"))
        
        # create the defult success message for the chatting_post
        content = "Congratulations to {} for creating a new chatroom \
            named {}".format(instance.owner_name, instance.name)   
        RoomMessage.objects.create(
            user=author, 
            belong_post = post,
            room=instance, 
            content=content
        )
            