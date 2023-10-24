
from django.urls import path
from chat.views import chat, chatfriend, chatroom, contracts, \
    groups, innerroom, my, settings, innergroup

  
urlpatterns = [
    path('my/', my, name='my'),
    path('chat/', chat, name='chat'),
    path('chat/<str:friend_name>/', chatfriend, name='chatfriend'),
    path('groups/', groups, name='groups'),
    path('chatroom/', chatroom, name='chatroom'),
    path('chatroom/<str:room_name>/<str:post_name>/', innerroom, name='innerroom'),
    path('contracts/', contracts, name='contracts'),
    path('settings/', settings, name='settings'),
    path('groups/<str:group_uid>/', innergroup, name='innergroup'),
]
