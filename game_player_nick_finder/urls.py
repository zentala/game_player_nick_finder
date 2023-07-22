# game_player_nick_finder/game_player_nick_finder/urls.py
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/profile/', views.account_profile, name='account_profile'),
    path('add/', views.add_game_and_character, name='add_game_and_character'),

    # Django Auth & Django Registration
    
    # Provided URLs are:
    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']

    # Choose one between those two: 
    path('accounts/', include('django_registration.backends.one_step.urls')), # no email verification:
    # path('accounts/', include('django_registration.backends.activation.urls')), # with email verification

    path('accounts/', include('django.contrib.auth.urls')),
]
