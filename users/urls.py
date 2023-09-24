from django.urls import path
from users import views


urlpatterns = [
    path('log/', views.log, name='log'),
]
