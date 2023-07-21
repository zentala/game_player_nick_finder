# game_player_nick_finder/game_player_nick_finder/urls.py
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]

urlpatterns = [
    path('', views.index, name='index'),
]