from django.urls import re_path

from .roomers import Roommers
# 允许我们组合和堆叠消费者
websocket_urlpatterns = [
    re_path(r'ws/chat/chatroom/(?P<room_name>\w+)$', Roommers.as_asgi()),
]