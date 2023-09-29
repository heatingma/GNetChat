from django.contrib import admin
from .models import Profile, Room, RoomMessage, Post, Tag

admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(RoomMessage)
admin.site.register(Tag)
admin.site.register(Post)