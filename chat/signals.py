from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Profile, RoomMessage, Room, Post, Tag, LINK
from django.shortcuts import get_object_or_404


DEFAULT_LINKS = [("https://i.sjtu.edu.cn/xtgl/login_slogin.html", "isjtu"),
                 ("https://mail.sjtu.edu.cn/zimbra", "jmail"), 
                 ("https://jbox.sjtu.edu.cn", "jbox"),
                 ("https://cnmooc.org/", "CNMOOC")]


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        user: User
        Profile.objects.create(user=user)
        for link in DEFAULT_LINKS:
            LINK.objects.create(url=link[0], name = link[1], user=user)
        
        
        
@receiver(post_save, sender=Room)
def create_rm_cp(sender, instance, created, **kwargs):
    if created:
        # create the default chatting_post
        author = User.objects.get(username=instance.owner_name)
        profile = get_object_or_404(Profile, user=author)
        post = Post.objects.create(
            title =  "chatting_" + instance.name,
            show_name = instance.show_name + "聊天室",
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
            