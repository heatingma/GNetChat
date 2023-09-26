from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Profile, RoomMessage, Room
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        
@receiver(post_save, sender=Room)
def create_roommessage(sender, instance, created, **kwargs):
    if created:
        content = "Congratulations to {} for creating a new chatroom \
            named {}".format(instance.owner_name, instance.name)
        RoomMessage.objects.create(
            user=get_object_or_404(User, username=instance.owner_name), 
            room=instance, 
            content=content
        )