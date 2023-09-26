
from django.urls import path
from chat import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my/', views.my, name='my'),
    path('groups/', views.groups, name='groups'),
    path('chatroom/', views.chatroom, name='chatroom'),
    path('chatroom/<str:room_name>/', views.innerroom, name='innerroom'),
    path('contracts/', views.contracts, name='contracts'),
    path('settings/', views.settings, name='settings'),
]
