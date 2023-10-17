from django.urls import re_path

from .roomers import Roommers, FRRoommers


websocket_urlpatterns = [
    re_path(r'ws/chat/chatroom/(?P<room_name>\w+)/(?P<post_name>\w+)/$', Roommers.as_asgi()),
    re_path(r'ws/chat/chat/(?P<friend_name>\w+)/$', FRRoommers.as_asgi()),
]