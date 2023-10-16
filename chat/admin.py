from django.contrib import admin
from .models import Profile, Room, RoomMessage, Post, Tag, Friend_Request, FMMessage, FriendRoom,LINK


admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(RoomMessage)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Friend_Request)
admin.site.register(FMMessage)
admin.site.register(FriendRoom)
admin.site.register(LINK)