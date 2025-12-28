# game_player_nick_finder/game_player_nick_finder/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views
from app.views import AccountProfileView, CharacterView, CharacterListView, CharacterEditView, GameListView, GameDetailView, GameCreateView, GameEditView, GameDeleteView, AboutView, CustomRegistrationView, MessageListView, RegistrationStep1View, RegistrationStep2View, RegistrationStep3View, RegistrationStep4View, UserCharactersListView, SendMessageView, GamePlayersView, PokeListView, SendPokeView, PokeDetailView, RespondPokeView, IgnorePokeView, BlockPokeView
from django_registration.backends.one_step.views import RegistrationView
from rest_framework.routers import DefaultRouter
# from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

from app import api_views

router = DefaultRouter()
router.register(r'games', api_views.GameViewSet)
router.register(r'characters', api_views.CharacterViewSet)
router.register(r'friend-requests', api_views.CharacterFriendRequestViewSet, basename='friend-request')
router.register(r'character-profiles', api_views.CharacterProfileViewSet, basename='character-profile')
router.register(r'user-profiles', api_views.UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('accounts/profile/', AccountProfileView.as_view(), name='account_profile'),
    path('profile/<str:username>/', views.UserProfileDisplayView.as_view(), name='user_profile_display'),
    path('characters/', CharacterListView.as_view(), name='character_list'),
	path('characters/<slug:game_slug>/', CharacterListView.as_view(), name='character_list_by_game'),
    path('character/add/', views.AddCharacterView.as_view(), name='add_character'),
    path('character/<str:nickname>-<str:hash_id>/', CharacterView.as_view(), name='character_detail'),
    path('character/<str:nickname>-<str:hash_id>/edit/', CharacterEditView.as_view(), name='character_edit'),
    path('character/<str:nickname>-<str:hash_id>/send-friend-request/', views.SendFriendRequestView.as_view(), name='send_friend_request'),
    path('character/<str:nickname>-<str:hash_id>/friends/', views.CharacterFriendListView.as_view(), name='character_friend_list'),
    path('character/<str:nickname>-<str:hash_id>/profile/edit/', views.CharacterProfileEditView.as_view(), name='character_profile_edit'),


    path('games/', GameListView.as_view(), name='game_list'),
    path('games/create/', GameCreateView.as_view(), name='game_create'),
    path('games/<slug:slug>/', GameDetailView.as_view(), name='game_detail'),
    path('games/<slug:slug>/players/', GamePlayersView.as_view(), name='game_players'),
    path('games/<slug:slug>/edit/', GameEditView.as_view(), name='game_edit'),
    path('games/<slug:slug>/delete/', GameDeleteView.as_view(), name='game_delete'),

    # Django Auth & Django Registration
    path('accounts/', include('allauth.urls')),

    # overwriting the default registration view; TODO not sure if this should be done this way
    # path('accounts/register/', CustomRegistrationView.as_view(), name='django_registration_register'),
    # path('accounts/register/', RegistrationView.as_view(template_name='django_registration/registration_form.html'), name='django_registration_register'),

	path('register/step1/', RegistrationStep1View.as_view(), name='register_step1'),
    path('register/step2/', RegistrationStep2View.as_view(), name='register_step2'),
    path('register/step3/', RegistrationStep3View.as_view(), name='register_step3'),
    path('register/step4/', RegistrationStep4View.as_view(), name='register_step4'),

    # path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # rmme

    path('account/characters/', UserCharactersListView.as_view(), name='account_characters_list'),

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

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/send/', SendMessageView.as_view(), name='send_message'),

    path('api/v1/', include(router.urls)),

	path('ui-demo/', views.ui_demo_view, name='ui_demo'),

    path('propose-game/', views.propose_game, name='propose_game'),
    path('proposed-games/', views.proposed_games_list, name='proposed_games_list'),
    path('proposed-games/vote/<int:game_id>/', views.vote_for_game, name='vote_for_game'),
    
    # Friend requests
    path('friends/requests/', views.FriendRequestListView.as_view(), name='friend_request_list'),
    path('friends/requests/<int:request_id>/accept/', views.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friends/requests/<int:request_id>/decline/', views.DeclineFriendRequestView.as_view(), name='decline_friend_request'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
