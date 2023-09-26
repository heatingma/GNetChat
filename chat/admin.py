from django.contrib import admin
from .models import Profile, Room, RoomMessage

admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(RoomMessage)