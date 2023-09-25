# 每次创建用户实例时自动创建配置文件实例
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Profile


@receiver(post_save, sender=User) # 当user保存后调用create_profile
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)