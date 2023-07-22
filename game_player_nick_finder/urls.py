# game_player_nick_finder/game_player_nick_finder/urls.py
from django.contrib import admin
from django.urls import path, include
from app import views
from app.views import AccountProfileView, CharacterView, CharacterListView, CharacterEditView, GameListView, GameDetailView, GameCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/profile/', AccountProfileView.as_view(), name='account_profile'),
    path('characters/', CharacterListView.as_view(), name='character_list'),
    path('character/add/', views.AddCharacterView.as_view(), name='add_character'),
    path('character/<str:user>-<str:nickname>/', CharacterView.as_view(), name='character_detail'),
    path('character/<str:user>-<str:nickname>/edit/', CharacterEditView.as_view(), name='character_edit'),
    
    path('games/', GameListView.as_view(), name='game_list'),
    path('games/create/', GameCreateView.as_view(), name='game_create'),
    path('games/<slug:slug>/', GameDetailView.as_view(), name='game_detail'),


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
