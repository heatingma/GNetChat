
from django.urls import path
from chat import views

urlpatterns = [
    path('my/', views.my, name='my'),
    path('chat/', views.chat, name='chat'),
    path('chat/<str:friend_name>/', views.chatfriend, name='chatfriend'),
    path('groups/', views.groups, name='groups'),
    path('chatroom/', views.chatroom, name='chatroom'),
    path('chatroom/<str:room_name>/<str:post_name>/', views.innerroom, name='innerroom'),
    path('contracts/', views.contracts, name='contracts'),
    path('settings/', views.settings, name='settings'),
    path('change-password/', views.change_password, name='change_password'),
]
