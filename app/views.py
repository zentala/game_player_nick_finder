from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django_registration.backends.one_step.views import RegistrationView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
import json

from .forms import (
    AddCharacterForm, CharacterFilterForm, UserEditForm, GameForm,
    CustomRegistrationForm, UserForm, MessageForm, ProposedGameForm,
    CharacterFriendRequestForm, CharacterProfileForm, PokeForm
)
from .models import (
    Game, Character, Message, CustomUser, GameCategory, ProposedGame, Vote,
    CharacterFriend, CharacterFriendRequest, CharacterProfile, Poke, PokeBlock,
    CharacterIdentityReveal, CharacterBlock
)
from .utils import can_send_poke, can_send_message




class BaseViewMixin:
	current_page = None

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['current_page'] = self.current_page
		return context



### Simple Views --------------------------------------

class IndexView(BaseViewMixin, TemplateView):
	current_page = 'home'
	template_name = 'index.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		# Get layout variant with priority: URL param > Session > Default
		layout = self.get_user_layout()
		
		context['layout'] = layout
		context['layout_variants'] = ['v0', 'v1', 'v2', 'v3']
		context['show_layout_switcher'] = self.should_show_switcher()
		context['debug'] = settings.DEBUG  # For template to show DEBUG badge
		
		# Mock data for testing (only for v1-v3)
		if layout != 'v0':
			context['mock_games'] = self.get_mock_games()
			context['mock_years'] = self.get_mock_years()
		
		return context
	
	def get_user_layout(self):
		"""
		Get layout for user with priority:
		1. URL param (highest priority, saves to session)
		2. Session storage (if user has saved preference)
		3. Default (v0)
		"""
		# Check URL param first
		url_layout = self.request.GET.get('layout', None)
		
		if url_layout:
			# Handle reset
			if url_layout == 'reset':
				if 'homepage_layout' in self.request.session:
					del self.request.session['homepage_layout']
					self.request.session.save()
				return 'v0'
			
			# Validate and save to session
			if url_layout in ['v0', 'v1', 'v2', 'v3']:
				self.request.session['homepage_layout'] = url_layout
				self.request.session.save()  # Explicitly save session
				return url_layout
		
		# Check session storage
		session_layout = self.request.session.get('homepage_layout', None)
		if session_layout and session_layout in ['v0', 'v1', 'v2', 'v3']:
			return session_layout
		
		# Default layout
		return 'v0'
	
	def should_show_switcher(self):
		"""
		Determine if layout switcher should be visible.
		Show switcher if:
		- URL param is present (user is actively switching)
		- User has saved layout preference (not default)
		- In development mode (DEBUG=True)
		- User is staff/superuser (developers)
		"""
		# Always show if URL param is present
		if self.request.GET.get('layout'):
			return True
		
		# Show if user has saved preference (not default)
		saved_layout = self.request.session.get('homepage_layout', None)
		if saved_layout and saved_layout != 'v0':
			return True
		
		# Always show in development mode
		if settings.DEBUG:
			return True
		
		# Show for staff/superuser (developers)
		if self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser):
			return True
		
		return False
	
	def get_mock_games(self):
		"""Return mock games data for testing"""
		return [
			{'id': 1, 'name': 'Counter-Strike', 'slug': 'counter-strike'},
			{'id': 2, 'name': 'World of Warcraft', 'slug': 'world-of-warcraft'},
			{'id': 3, 'name': 'League of Legends', 'slug': 'league-of-legends'},
			{'id': 4, 'name': 'Minecraft', 'slug': 'minecraft'},
			{'id': 5, 'name': 'Diablo II', 'slug': 'diablo-ii'},
			{'id': 6, 'name': 'StarCraft', 'slug': 'starcraft'},
			{'id': 7, 'name': 'Warcraft III', 'slug': 'warcraft-iii'},
			{'id': 8, 'name': 'Quake', 'slug': 'quake'},
		]
	
	def get_mock_years(self):
		"""Return years for Time Machine slider"""
		return list(range(1990, 2025))  # 1990-2024

class AboutView(BaseViewMixin, TemplateView):
	current_page = 'about'
	template_name = 'about.html'



### Registration --------------------------------------

class CustomRegistrationView(RegistrationView):
	form_class = CustomRegistrationForm
	template_name = 'django_registration/registration_form.html'
	current_page = 'register'

class RegistrationStep1View(BaseViewMixin, FormView):
	form_class = UserForm  # Twój formularz dla kroku 1
	template_name = 'django_registration/registration_step1.html'
	current_page = 'register_step1'

	def form_valid(self, form):
		# Zapisz dane formularza w sesji
		self.request.session['register_step1_data'] = form.cleaned_data
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('register_step2')  # URL do kroku 2

class RegistrationStep2View(BaseViewMixin, FormView):
	form_class = UserForm  # Formularz dla kroku 2
	template_name = 'django_registration/registration_step1.html'
	current_page = 'register_step2'

	def form_valid(self, form):
		# Zapisz dane formularza z kroku 2 w sesji
		self.request.session['register_step2_data'] = form.cleaned_data
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('register_step3')  # URL do kroku 3

class RegistrationStep3View(BaseViewMixin, FormView):
	form_class = UserForm  # Formularz dla kroku 2
	template_name = 'django_registration/registration_step1.html'
	current_page = 'register_step3'

	def form_valid(self, form):
		# Zapisz dane formularza z kroku 2 w sesji
		self.request.session['register_step2_data'] = form.cleaned_data
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('register_step4')  # URL do kroku 3

class RegistrationStep4View(BaseViewMixin, FormView):
	form_class = UserForm  # Formularz dla kroku 2
	template_name = 'django_registration/registration_step1.html'
	current_page = 'register_step4'

	def form_valid(self, form):
		# Zapisz dane formularza z kroku 2 w sesji
		self.request.session['register_step2_data'] = form.cleaned_data
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('register_step3')  # URL do kroku 3

class UserProfileDisplayView(DetailView):
	"""Display public user profile with visibility checks"""
	model = CustomUser
	template_name = 'profile/user_profile_display.html'
	context_object_name = 'profile_user'
	slug_field = 'username'
	slug_url_kwarg = 'username'
	
	def get_object(self, queryset=None):
		profile_user = super().get_object(queryset)
		viewer = self.request.user
		
		# Check visibility
		if profile_user.profile_visibility == 'PRIVATE' and (not viewer.is_authenticated or viewer != profile_user):
			raise PermissionDenied(_('This profile is private.'))
		
		if profile_user.profile_visibility == 'FRIENDS_ONLY' and (not viewer.is_authenticated or viewer != profile_user):
			# Check if users are friends through any characters
			if not self._are_friends(profile_user, viewer):
				raise PermissionDenied(_('This profile is only visible to friends.'))
		
		return profile_user
	
	def _are_friends(self, user1, user2):
		"""Check if users are friends through any characters"""
		if not user2.is_authenticated:
			return False
		
		user1_characters = Character.objects.filter(user=user1)
		user2_characters = Character.objects.filter(user=user2)
		
		return CharacterFriend.objects.filter(
			(Q(character1__in=user1_characters) & Q(character2__in=user2_characters)) |
			(Q(character1__in=user2_characters) & Q(character2__in=user1_characters))
		).exists()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		profile_user = self.get_object()
		context['title'] = f'{profile_user.username} - Profile'
		context['content_template'] = 'profile/user_profile_display_content.html'
		
		# Get user's characters
		context['user_characters'] = Character.objects.filter(user=profile_user)
		
		return context

class AccountProfileView(LoginRequiredMixin, View):
	template_name = 'account_profile.html'

	def get(self, request):
		# Force loading the user from database using username
		User = get_user_model()
		user = User.objects.get(username=request.user.username)

		print(f"User type after loading: {type(user)}")  # Debug line
		print(f"User ID: {user.id}")       # Debug line
		print(f"User's username: {user.username}")  # Debug line

		try:
			characters = Character.objects.filter(user=user)
		except Exception as e:
			print(f"Error fetching characters: {e}")
			characters = []

		form = UserEditForm(instance=user)

		context = {
			'user': user,
			'characters': characters,
			'form': form,
			'title': 'User Profile',
			'content_template': 'account/profile_content.html',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		User = get_user_model()
		user = User.objects.get(username=request.user.username)
		characters = Character.objects.filter(user=user)
		form = UserEditForm(request.POST, request.FILES, instance=user)  # Add request.FILES

		if form.is_valid():
			user = form.save()
			messages.success(request, 'Profile updated successfully!')
			return redirect('account_profile')

		context = {
			'user': user,
			'characters': characters,
			'form': form,
			'title': 'User Profile',
			'content_template': 'account/profile_content.html',
		}
		return render(request, self.template_name, context)



### Characters ----------------------------------------

class AddCharacterView(BaseViewMixin, LoginRequiredMixin, CreateView):
	model = Character
	form_class = AddCharacterForm
	template_name = 'characters/add_character.html'
	success_url = reverse_lazy('character_list')
	current_page = 'characters'

	def get_initial(self):
		initial = super().get_initial()
		game_id = self.request.GET.get('game')
		if game_id:
			try:
				game = Game.objects.get(id=game_id)
				initial['game'] = game
			except Game.DoesNotExist:
				pass
		return initial

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.object and self.object.pk:
			context['title'] = _("Edit Character")
			context['back_url'] = reverse('character_detail', kwargs={
				'user': self.object.user.username,
				'nickname': self.object.nickname
			})
		else:
			context['title'] = _("New Character")

			# Zachowaj parametr game w linku powrotu
			if self.request.GET.get('game'):
				context['back_url'] = reverse('message_list') + f"?character={self.request.GET.get('character')}"
			else:
				context['back_url'] = reverse('character_list')

		context['back_label'] = _("Back")
		context['content_template'] = 'characters/character_form_content.html'
		return context

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			character = form.save(commit=False)
			character.user = request.user
			character.save()

			# Jeśli tworzymy postać z czatu, wróć do czatu
			character_id = request.GET.get('character')
			if character_id:
				return redirect(reverse('message_list') + f'?character={character_id}')

			return redirect(self.success_url)

		context = self.get_context_data()
		context['form'] = form
		return render(request, self.template_name, context)


class CharacterListView(BaseViewMixin, ListView):
	model = Character
	template_name = 'characters/character_list.html'
	current_page = 'characters'
	context_object_name = 'characters'
	paginate_by = 10

	def get_queryset(self):
		form = CharacterFilterForm(self.request.GET)
		game_slug = self.kwargs.get('game_slug')  # Pobieranie sluga gry z URL

		queryset = Character.objects.select_related('user', 'game').all()

		if form.is_valid():
			game = form.cleaned_data.get('game') or game_slug
			year = form.cleaned_data['year']
			nickname = form.cleaned_data['nickname']

			if game:
				if isinstance(game, str):  # jeśli dostaliśmy slug
					queryset = queryset.filter(game__slug=game)
				else:  # jeśli dostaliśmy obiekt Game
					queryset = queryset.filter(game=game)

			if year is not None:
				queryset = queryset.filter(
					Q(year_started__lte=year) & (Q(year_ended__gte=year) | Q(year_ended__isnull=True)) |
					(Q(year_started__isnull=True) & Q(year_ended__isnull=True))
				)

			if nickname:
				queryset = queryset.filter(nickname__icontains=nickname)

			return queryset

		elif game_slug:
			# Filtrowanie tylko na podstawie sluga, gdy formularz nie jest prawidłowy
			return queryset.filter(game__slug=game_slug)

		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		game_slug = self.kwargs.get('game_slug')
		game_id = self.request.GET.get('game')

		# Sprawdź czy mamy parametry formularza w URL
		initial_data = {}
		if self.request.GET.get('nickname'):
			initial_data['nickname'] = self.request.GET.get('nickname')
		if game_id:
			initial_data['game'] = game_id
		if self.request.GET.get('year'):
			initial_data['year'] = self.request.GET.get('year')
		else:
			# Domyślny rok to 2000
			initial_data['year'] = 2000

		# Informacje o grze do banera
		if game_slug:
			try:
				game = Game.objects.get(slug=game_slug)
				initial_data['game'] = game.id
				context['game'] = game
				context['game_slug'] = game_slug
			except Game.DoesNotExist:
				pass
		elif game_id:
			try:
				game = Game.objects.get(id=game_id)
				context['game'] = game
				context['game_slug'] = game.slug
			except Game.DoesNotExist:
				pass

		# Dodaj mapowanie ID gier do ich slugów (serialized as JSON string)
		game_slugs_dict = {str(g.id): g.slug for g in Game.objects.all()}
		context['game_slugs_json'] = json.dumps(game_slugs_dict)

		# Stosuj wszystkie ustalone initial_data
		if initial_data:
			context['form'] = CharacterFilterForm(initial=initial_data)
		else:
			context['form'] = CharacterFilterForm(initial={'year': 2000})

		# Dodaj informację o aktywnych filtrach dla lepszej UX
		context['has_filters'] = bool(self.request.GET.get('nickname') or game_id or self.request.GET.get('year') or game_slug)

		return context


class CharacterView(BaseViewMixin, DetailView):
	current_page = 'characters'
	model = Character
	template_name = 'characters/character_detail.html'
	context_object_name = 'character'

	def get_object(self, queryset=None):
		nickname = self.kwargs['nickname']
		hash_id = self.kwargs['hash_id']
		return get_object_or_404(Character, nickname=nickname, hash_id=hash_id)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		character = self.get_object()
		context['title'] = character.nickname
		context['content_template'] = 'characters/character_detail_content.html'
		context['back_url'] = reverse('account_characters_list')
		context['back_label'] = _('Back to My Characters')
		
		# Check if user is logged in
		if self.request.user.is_authenticated:
			user = self.request.user
			user_characters = Character.objects.filter(user=user)
			
			# Check if any of user's characters is friend with this character
			is_friend = CharacterFriend.objects.filter(
				Q(character1=character, character2__in=user_characters) |
				Q(character2=character, character1__in=user_characters)
			).exists()
			
			# Check if there's a pending friend request
			pending_request = CharacterFriendRequest.objects.filter(
				receiver_character=character,
				sender_character__in=user_characters,
				status='PENDING'
			).first()
			
			# Check if user can send request (not own character, not already friend)
			can_send_request = (
				character.user != user and 
				not is_friend and 
				pending_request is None
			)
			
			# Check if messaging is unlocked (mutual POKE exchange)
			can_send_full_message = False
			matching_character = None
			if character.user != user and user_characters.exists():
				matching_character = user_characters.filter(game=character.game).first()
				if matching_character:
					can_send_full_message, _ = can_send_message(matching_character, character)
			
			# Check if character is blocked by any of user's characters
			is_blocked_by_user = False
			blocking_block = None
			if character.user != user and user_characters.exists():
				blocking_block = CharacterBlock.objects.filter(
					blocker_character__in=user_characters,
					blocked_character=character
				).first()
				is_blocked_by_user = blocking_block is not None
			
			context['is_friend'] = is_friend
			context['pending_request'] = pending_request
			context['can_send_request'] = can_send_request
			context['user_characters'] = user_characters  # For selecting which character sends request
			context['can_send_full_message'] = can_send_full_message
			context['matching_character'] = matching_character
			context['is_blocked_by_user'] = is_blocked_by_user
			context['blocking_block'] = blocking_block
		
		# Get character profile if exists
		try:
			context['character_profile'] = character.profile
		except CharacterProfile.DoesNotExist:
			context['character_profile'] = None

		if self.request.user == character.user:
			context['show_action'] = True
			context['action_url'] = reverse('character_edit', kwargs={
				'nickname': character.nickname,
				'hash_id': character.hash_id
			})
			context['action_label'] = _('Edit Character')

		return context

class FriendRequestListView(LoginRequiredMixin, ListView):
	"""List all friend requests for user's characters"""
	model = CharacterFriendRequest
	template_name = 'friends/friend_request_list.html'
	context_object_name = 'friend_requests'
	current_page = 'friends'
	
	def get_queryset(self):
		user_characters = Character.objects.filter(user=self.request.user)
		
		# Get requests received by user's characters
		return CharacterFriendRequest.objects.filter(
			receiver_character__in=user_characters,
			status='PENDING'
		).select_related('sender_character', 'sender_character__game', 'sender_character__user').order_by('-sent_date')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = _('Friend Requests')
		context['back_url'] = reverse('account_profile')
		context['back_label'] = _('Back to Profile')
		context['content_template'] = 'friends/friend_request_list_content.html'
		return context


class AcceptFriendRequestView(LoginRequiredMixin, View):
	"""Accept a friend request"""
	
	def post(self, request, request_id):
		friend_request = get_object_or_404(
			CharacterFriendRequest,
			id=request_id,
			receiver_character__user=request.user,
			status='PENDING'
		)
		
		# Create friendship
		CharacterFriend.objects.create(
			character1=friend_request.sender_character,
			character2=friend_request.receiver_character
		)
		
		# Update request status
		friend_request.status = 'ACCEPTED'
		friend_request.save()
		
		messages.success(request, f'Accepted friend request from {friend_request.sender_character.nickname}!')
		return redirect('friend_request_list')


class DeclineFriendRequestView(LoginRequiredMixin, View):
	"""Decline a friend request"""
	
	def post(self, request, request_id):
		friend_request = get_object_or_404(
			CharacterFriendRequest,
			id=request_id,
			receiver_character__user=request.user,
			status='PENDING'
		)
		
		friend_request.status = 'DECLINED'
		friend_request.save()
		
		messages.info(request, f'Declined friend request from {friend_request.sender_character.nickname}.')
		return redirect('friend_request_list')


class SendFriendRequestView(LoginRequiredMixin, View):
	"""Handle friend request sending from UI"""
	
	def post(self, request, nickname, hash_id):
		receiver_character = get_object_or_404(Character, nickname=nickname, hash_id=hash_id)
		sender_character_id = request.POST.get('sender_character')
		message = request.POST.get('message', '')
		
		try:
			sender_character = Character.objects.get(id=sender_character_id, user=request.user)
		except Character.DoesNotExist:
			messages.error(request, 'Invalid character selected.')
			return redirect('character_detail', nickname=nickname, hash_id=hash_id)
		
		# Check if already friends
		if CharacterFriend.objects.filter(
			Q(character1=sender_character, character2=receiver_character) |
			Q(character1=receiver_character, character2=sender_character)
		).exists():
			messages.error(request, 'You are already friends with this character.')
			return redirect('character_detail', nickname=nickname, hash_id=hash_id)
		
		# Check if request already exists
		if CharacterFriendRequest.objects.filter(
			sender_character=sender_character,
			receiver_character=receiver_character,
			status='PENDING'
		).exists():
			messages.info(request, 'Friend request already sent.')
			return redirect('character_detail', nickname=nickname, hash_id=hash_id)
		
		# Check if receiver has blocked sender
		if CharacterBlock.objects.filter(
			blocker_character=receiver_character,
			blocked_character=sender_character
		).exists():
			messages.error(request, _('You cannot send a friend request to this character.'))
			return redirect('character_detail', nickname=nickname, hash_id=hash_id)
		
		# Create friend request
		friend_request = CharacterFriendRequest.objects.create(
			sender_character=sender_character,
			receiver_character=receiver_character,
			message=message,
			status='PENDING'
		)
		
		messages.success(request, f'Friend request sent to {receiver_character.nickname}!')
		return redirect('character_detail', nickname=nickname, hash_id=hash_id)

class CharacterFriendListView(LoginRequiredMixin, ListView):
	"""List all friends for a specific character"""
	model = CharacterFriend
	template_name = 'friends/character_friend_list.html'
	context_object_name = 'friendships'
	current_page = 'friends'
	
	def get_queryset(self):
		# Store character as instance variable for use in get_context_data
		self.character = get_object_or_404(
			Character,
			nickname=self.kwargs['nickname'],
			hash_id=self.kwargs['hash_id'],
			user=self.request.user
		)
		
		# Return QuerySet (not a list) - Django ListView requires QuerySet for pagination
		return CharacterFriend.objects.filter(
			Q(character1=self.character) | Q(character2=self.character)
		).select_related('character1', 'character1__game', 'character2', 'character2__game')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		# Get the character (either from instance variable or query)
		character = getattr(self, 'character', None)
		if not character:
			character = get_object_or_404(
				Character,
				nickname=self.kwargs['nickname'],
				hash_id=self.kwargs['hash_id']
			)
		
		# Process friendships queryset/list into friend_data format expected by template
		# self.object_list contains the queryset results (list if paginated, queryset otherwise)
		friendships_list = list(self.object_list) if hasattr(self, 'object_list') else []
		friend_data_list = []
		for friendship in friendships_list:
			friend_char = friendship.character2 if friendship.character1 == character else friendship.character1
			friend_data_list.append({
				'character': friend_char,
				'friendship': friendship
			})
		
		# Replace friendships in context with processed list
		context['friendships'] = friend_data_list
		context['character'] = character
		context['title'] = f'{character.nickname} - Friends'
		context['back_url'] = reverse('character_detail', kwargs={
			'nickname': character.nickname,
			'hash_id': character.hash_id
		})
		context['back_label'] = _('Back to Character')
		context['content_template'] = 'friends/character_friend_list_content.html'
		return context

class CharacterProfileEditView(LoginRequiredMixin, UpdateView):
	"""Edit character custom profile"""
	model = CharacterProfile
	form_class = CharacterProfileForm
	template_name = 'characters/character_profile_edit.html'
	current_page = 'characters'
	
	def get_object(self, queryset=None):
		character = get_object_or_404(
			Character,
			nickname=self.kwargs['nickname'],
			hash_id=self.kwargs['hash_id'],
			user=self.request.user
		)
		profile, created = CharacterProfile.objects.get_or_create(character=character)
		return profile
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		character = get_object_or_404(
			Character,
			nickname=self.kwargs['nickname'],
			hash_id=self.kwargs['hash_id']
		)
		context['character'] = character
		context['title'] = f'Edit Profile - {character.nickname}'
		context['back_url'] = reverse('character_detail', kwargs={
			'nickname': character.nickname,
			'hash_id': character.hash_id
		})
		context['back_label'] = _('Back to Character')
		context['content_template'] = 'characters/character_profile_edit_content.html'
		return context
	
	def get_success_url(self):
		character = self.object.character
		messages.success(self.request, 'Character profile updated successfully!')
		return reverse('character_detail', kwargs={
			'nickname': character.nickname,
			'hash_id': character.hash_id
		})

class CharacterEditView(BaseViewMixin, LoginRequiredMixin, UpdateView):
	current_page = 'characters'
	template_name = 'characters/add_character.html'
	model = Character
	form_class = AddCharacterForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		character = self.get_object()
		context['title'] = _("Edit Character")
		context['back_url'] = reverse('character_detail', kwargs={
			'nickname': character.nickname,
			'hash_id': character.hash_id
		})
		context['back_label'] = _("Back to Character")
		context['content_template'] = 'characters/character_form_content.html'

		# Dodaj informację dla admina edytującego cudzą postać
		if self.request.user.is_staff and character.user != self.request.user:
			context['admin_message'] = {
				'text': _('You are editing another user\'s character as an administrator.'),
				'owner': character.user.username
			}

		return context

	def get_object(self):
		nickname = self.kwargs['nickname']
		hash_id = self.kwargs['hash_id']
		character = get_object_or_404(Character, nickname=nickname, hash_id=hash_id)

		# Sprawdź uprawnienia do edycji
		if character.user != self.request.user and not self.request.user.is_staff:
			raise PermissionDenied(_("You don't have permission to edit this character"))

		return character

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.form_class(request.POST, request.FILES, instance=self.object)
		if form.is_valid():
			character = form.save()
			messages.success(request, _('Character updated successfully!'))
			return redirect(self.get_success_url())

		context = self.get_context_data()
		context['form'] = form
		return render(request, self.template_name, context)

	def get_success_url(self):
		return reverse('character_detail', kwargs={
			'nickname': self.object.nickname,
			'hash_id': self.object.hash_id
		})



### Games- --------------------------------------------

class GameListView(BaseViewMixin, ListView):
	current_page = 'games'
	model = Game
	template_name = 'games/games_list.html'
	context_object_name = 'games'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		# Utwórz słownik z liczbą postaci dla każdej gry
		characters_count = {}
		for game in context['games']:
			characters_count[game.id] = Character.objects.filter(game=game).count()

		context['characters_count'] = characters_count
		return context

class GameDetailView(BaseViewMixin, DetailView):
	current_page = 'games'
	model = Game
	template_name = 'games/game_detail.html'
	context_object_name = 'game'
	slug_field = 'slug'
	slug_url_kwarg = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		game = self.get_object()

		# Pobierz listę graczy dla tej gry
		players = Character.objects.filter(game=game).select_related('user')

		# Statystyki
		context['players_count'] = players.count()
		context['active_players_count'] = players.filter(year_ended__isnull=True).count()
		context['inactive_players_count'] = players.filter(year_ended__isnull=False).count()

		# Lista ostatnich graczy (maksymalnie 5)
		context['recent_players'] = players.order_by('-id')[:5]

		# Dane dla default container
		context['title'] = game.name
		context['back_url'] = reverse('game_list')
		context['back_label'] = _('Back to Games')
		context['content_template'] = 'games/game_detail_content.html'

		# Jeśli użytkownik jest adminem, dodaj link do edycji
		if self.request.user.is_staff:
			context['show_action'] = True
			context['action_url'] = reverse('game_edit', kwargs={'slug': game.slug})
			context['action_label'] = _('Edit Game')

			# Dodaj drugi link do zarządzania graczami
			context['second_action_url'] = reverse('game_players', kwargs={'slug': game.slug})
			context['second_action_label'] = _('Manage Players')

		return context

class GamePlayersView(BaseViewMixin, ListView):
	model = Character
	template_name = 'games/game_players.html'
	context_object_name = 'characters'
	current_page = 'games'
	paginate_by = 20

	def get_queryset(self):
		game_slug = self.kwargs.get('slug')
		return Character.objects.filter(game__slug=game_slug).select_related('user', 'game')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		game = get_object_or_404(Game, slug=self.kwargs.get('slug'))
		context['game'] = game
		context['title'] = f'Players of {game.name}'
		context['content_template'] = 'games/game_players_content.html'
		context['back_url'] = reverse('game_detail', kwargs={'slug': game.slug})
		context['back_label'] = _('Back to Game')
		return context

class GameFormViewMixin:
	model = Game
	template_name = 'games/game_form.html'
	form_class = GameForm
	success_url = reverse_lazy('game_list')

	def form_valid(self, form):
		form.save()
		messages.success(self.request, "Game created successfully!")
		response = super().form_valid(form)
		return response

class GameCreateView(BaseViewMixin, GameFormViewMixin, FormView):
	current_page = 'games'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['action'] = 'create'
		return context

class GameEditView(BaseViewMixin, GameFormViewMixin, UpdateView):
	current_page = 'games'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form_title'] = 'Edit Game'
		context['title'] = f'Edit {self.object.name}'
		context['content_template'] = 'games/game_form_content.html'
		context['back_url'] = reverse('game_detail', kwargs={'slug': self.object.slug})
		context['back_label'] = 'Back to Game'
		return context

class GameDeleteView(BaseViewMixin, DeleteView):
	current_page = 'games'
	model = Game
	template_name = 'games/game_confirm_delete.html'
	success_url = '/games/'  # URL to redirect after successful deletion

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = f'Delete {self.object.name}'
		context['content_template'] = 'games/game_delete_content.html'
		context['back_url'] = reverse('game_detail', kwargs={'slug': self.object.slug})
		context['back_label'] = 'Cancel'
		return context

	def delete(self, request, *args, **kwargs):
		messages.success(request, 'Game successfully deleted.')
		return super().delete(request, *args, **kwargs)

### Played Games --------------------------------------
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'messages/message_list.html'
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        """Mark messages as read when viewing a thread"""
        response = super().get(request, *args, **kwargs)
        
        thread_id = request.GET.get('thread_id')
        if thread_id:
            user_characters = Character.objects.filter(user=request.user)
            Message.objects.filter(
                thread_id=thread_id,
                receiver_character__in=user_characters,
                is_read=False
            ).update(is_read=True, read_at=timezone.now())
        
        return response

    def get_queryset(self):
        thread_id = self.request.GET.get('thread_id')
        receiver_character_id = self.request.GET.get('character')
        user_characters = Character.objects.filter(user=self.request.user)

        if thread_id:
            # Jeśli mamy thread_id, pobierz wszystkie wiadomości z tej konwersacji
            return Message.objects.filter(thread_id=thread_id).order_by('sent_date')
        elif receiver_character_id:
            # Jeśli mamy character_id, znajdź lub utwórz nowy wątek
            try:
                receiver_character = Character.objects.get(id=receiver_character_id)
                # Znajdź istniejący wątek
                existing_thread = Message.objects.filter(
                    models.Q(sender_character__in=user_characters, receiver_character=receiver_character) |
                    models.Q(receiver_character__in=user_characters, sender_character=receiver_character)
                ).values_list('thread_id', flat=True).first()

                if existing_thread:
                    return Message.objects.filter(thread_id=existing_thread).order_by('sent_date')
                else:
                    return Message.objects.none()
            except Character.DoesNotExist:
                return Message.objects.none()
        else:
            # No thread_id or character_id - return empty queryset
            # Conversation list is now handled in get_context_data() for sidebar display
            return Message.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver_character_id = self.request.GET.get('character')
        sender_character_id = self.request.GET.get('sender')
        thread_id = self.request.GET.get('thread_id')
        user_characters = Character.objects.filter(user=self.request.user)

        if not user_characters.exists():
            context['error_message'] = _("You need to create a character first to send messages.")
            return context

        # Build conversation list for sidebar
        user_threads = Message.objects.filter(
            models.Q(sender_character__in=user_characters) |
            models.Q(receiver_character__in=user_characters)
        ).values_list('thread_id', flat=True).distinct()

        conversations = []
        for thread_id_value in user_threads:
            thread_messages = Message.objects.filter(
                thread_id=thread_id_value
            ).select_related(
                'sender_character',
                'receiver_character',
                'sender_character__game',
                'receiver_character__game'
            ).order_by('-sent_date')

            if thread_messages.exists():
                latest_message = thread_messages.first()

                # Determine other character (not user's character)
                if latest_message.sender_character in user_characters:
                    other_character = latest_message.receiver_character
                else:
                    other_character = latest_message.sender_character

                # Count unread messages for this thread
                unread_count = Message.objects.filter(
                    thread_id=thread_id_value,
                    receiver_character__in=user_characters,
                    is_read=False
                ).count()

                # Get message preview (first 100 chars)
                preview = latest_message.content[:100]
                if len(latest_message.content) > 100:
                    preview += "..."

                conversations.append({
                    'thread_id': thread_id_value,
                    'other_character': other_character,
                    'latest_message': latest_message,
                    'unread_count': unread_count,
                    'message_preview': preview,
                })

        # Sort by latest message date (newest first)
        conversations.sort(
            key=lambda x: x['latest_message'].sent_date,
            reverse=True
        )

        context['conversations'] = conversations
        context['current_thread_id'] = thread_id
        context['current_character_id'] = receiver_character_id

        if receiver_character_id:
            try:
                receiver_character = Character.objects.get(id=receiver_character_id)
                context['receiver_character'] = receiver_character

                # Znajdź postacie użytkownika w tej samej grze co odbiorca
                matching_characters = user_characters.filter(game=receiver_character.game)
                context['matching_characters'] = matching_characters

                if not matching_characters.exists():
                    # Jeśli użytkownik nie ma postaci w tej samej grze
                    context['no_matching_characters'] = True
                    game_url = reverse('add_character') + f'?game={receiver_character.game.id}&character={receiver_character.id}'
                    context['create_character_url'] = game_url
                elif matching_characters.count() == 1:
                    # Jeśli użytkownik ma tylko jedną postać w tej samej grze
                    matching_char = matching_characters.first()
                    context['sender_character'] = matching_char
                    
                    # Check if messaging is unlocked
                    can_send, reason = can_send_message(matching_char, receiver_character)
                    context['can_send_message'] = can_send
                    if not can_send:
                        context['suggest_poke'] = True
                        context['poke_url'] = f"{reverse('send_poke')}?character={receiver_character.id}&sender_character={matching_char.id}"
                elif sender_character_id and matching_characters.filter(id=sender_character_id).exists():
                    # Jeśli wybrano konkretną postać do wysyłania
                    matching_char = matching_characters.get(id=sender_character_id)
                    context['sender_character'] = matching_char
                    
                    # Check if messaging is unlocked
                    can_send, reason = can_send_message(matching_char, receiver_character)
                    context['can_send_message'] = can_send
                    if not can_send:
                        context['suggest_poke'] = True
                        context['poke_url'] = f"{reverse('send_poke')}?character={receiver_character.id}&sender_character={matching_char.id}"

                # Check if identity is revealed for this conversation
                identity_revealed = False
                if sender_character:
                    from .models import CharacterIdentityReveal
                    identity_revealed = CharacterIdentityReveal.objects.filter(
                        revealing_character=sender_character,
                        revealed_to_character=receiver_character,
                        is_active=True
                    ).exists()
                    context['identity_revealed'] = identity_revealed
                    context['identity_reveal'] = CharacterIdentityReveal.objects.filter(
                        revealing_character=sender_character,
                        revealed_to_character=receiver_character
                    ).first()
                
                # Check if identity is revealed for this conversation
                identity_revealed = False
                identity_reveal = None
                if 'sender_character' in context:
                    sender_character = context['sender_character']
                    from .models import CharacterIdentityReveal
                    identity_reveal = CharacterIdentityReveal.objects.filter(
                        revealing_character=sender_character,
                        revealed_to_character=receiver_character
                    ).first()
                    identity_revealed = identity_reveal and identity_reveal.is_active if identity_reveal else False
                    context['identity_revealed'] = identity_revealed
                    context['identity_reveal'] = identity_reveal
                
                context['form'] = MessageForm(
                    user=self.request.user,
                    sender_character=context.get('sender_character'),
                    receiver_character=receiver_character,
                    initial={'receiver_character': receiver_character}
                )
            except Character.DoesNotExist:
                pass
        elif thread_id:
            context['thread_id'] = thread_id
            context['form'] = MessageForm(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        """Obsługuje wysyłanie wiadomości bezpośrednio z widoku listy wiadomości"""
        receiver_character_id = request.POST.get('receiver_character')
        sender_character_id = request.POST.get('sender_character')
        
        sender_character = None
        receiver_character = None
        
        if sender_character_id:
            try:
                sender_character = Character.objects.get(id=sender_character_id, user=request.user)
            except Character.DoesNotExist:
                pass
        
        if receiver_character_id:
            try:
                receiver_character = Character.objects.get(id=receiver_character_id)
            except Character.DoesNotExist:
                pass
        
        form = MessageForm(
            request.POST, 
            user=request.user,
            sender_character=sender_character,
            receiver_character=receiver_character
        )

        if form.is_valid():
            message = form.save(commit=False)
            sender_character_id = request.POST.get('sender_character')

            # Użyj wybranej postaci jako nadawcy
            if sender_character_id:
                try:
                    sender_character = Character.objects.get(id=sender_character_id, user=request.user)
                    message.sender_character = sender_character
                except Character.DoesNotExist:
                    messages.error(request, _("Selected character not found."))
                    redirect_url = request.get_full_path()
                    return redirect(redirect_url)
            else:
                # Jeśli nie wybrano konkretnej postaci, spróbuj znaleźć pasującą do gry odbiorcy
                receiver_character = form.cleaned_data['receiver_character']
                matching_character = Character.objects.filter(
                    user=request.user, game=receiver_character.game
                ).first()

                if not matching_character:
                    messages.error(request, _("You need to have a character in the same game to send messages."))
                    return redirect(f'{reverse("add_character")}?game={receiver_character.game.id}')

                message.sender_character = matching_character

            # Sprawdź czy istnieje już wątek dla tej pary rozmówców
            thread_id = request.GET.get('thread_id')

            if thread_id:
                # Użyj istniejącego thread_id jeśli jest dostępny
                message.thread_id = thread_id
            else:
                # Spróbuj znaleźć istniejący wątek dla tych rozmówców
                existing_thread = Message.objects.filter(
                    models.Q(
                        sender_character=message.sender_character,
                        receiver_character=message.receiver_character
                    ) | models.Q(
                        sender_character=message.receiver_character,
                        receiver_character=message.sender_character
                    )
                ).values_list('thread_id', flat=True).first()

                if existing_thread:
                    # Użyj istniejącego thread_id
                    message.thread_id = existing_thread
                # W przeciwnym razie zostanie wygenerowane nowe thread_id

            message.save()

            # Przekieruj z powrotem do konwersacji z zachowaniem informacji o nadawcy
            if sender_character_id:
                redirect_url = f"{reverse('message_list')}?character={message.receiver_character.id}&sender={sender_character_id}"
            else:
                redirect_url = f"{reverse('message_list')}?character={message.receiver_character.id}"

            # Zawsze dołącz thread_id do URL, aby zapewnić spójność konwersacji
            redirect_url += f"&thread_id={message.thread_id}"

            return redirect(redirect_url)

        # Jeśli formularz jest nieprawidłowy, pokaż stronę z błędami
        context = self.get_context_data(object_list=self.get_queryset(), form=form)
        return self.render_to_response(context)

class UserCharactersListView(BaseViewMixin, ListView):
    model = Character
    template_name = 'characters/user_characters_list.html'
    context_object_name = 'characters'

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Characters'
        context['content_template'] = 'characters/user_characters_content.html'
        context['show_action'] = True
        context['action_url'] = reverse('add_character')
        context['action_label'] = 'Add Character'
        return context

### Mocked Messages ---------------------------------
def ui_demo_view(request):
    if settings.ENABLE_MOCK_MESSAGES:
        # Dodaj przykładowe wiadomości
        messages.debug(request, "This is a debug message.")
        messages.success(request, "This is a success message.")
        messages.error(request, "This is an error message.")
        messages.warning(request, "This is a warning message.")
        messages.info(request, "This is an info message.")

    # Renderuj stronę z wiadomościami
    return render(request, 'base.html')

class SendMessageView(LoginRequiredMixin, FormView):
    template_name = 'messages/send_message.html'
    form_class = MessageForm
    success_url = reverse_lazy('message_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        # Dodaj initial data jeśli mamy character_id w URL
        character_id = self.request.GET.get('character')
        if character_id:
            try:
                receiver_character = Character.objects.get(id=character_id)
                if not kwargs.get('initial'):
                    kwargs['initial'] = {}
                kwargs['initial']['receiver_character'] = receiver_character
            except Character.DoesNotExist:
                pass

        return kwargs

    def form_valid(self, form):
        message = form.save(commit=False)
        user_characters = Character.objects.filter(user=self.request.user)

        if not user_characters.exists():
            messages.error(self.request, "You need to create a character first to send messages.")
            return redirect('character_list')

        # Użyj postaci, która pasuje do gry odbiorcy
        receiver_character = form.cleaned_data['receiver_character']
        matching_character = user_characters.filter(game=receiver_character.game).first()

        if not matching_character:
            messages.error(self.request, "You need to have a character in the same game to send messages.")
            return redirect('character_list')

        # Check if messaging is unlocked (mutual POKE exchange)
        can_send, reason = can_send_message(matching_character, receiver_character)
        if not can_send:
            messages.warning(
                self.request,
                _("You must exchange POKEs before sending messages. ") + str(reason)
            )
            return redirect(f"{reverse('send_poke')}?character={receiver_character.id}&sender_character={matching_character.id}")

        message.sender_character = matching_character
        thread_id = self.request.GET.get('thread_id')

        if thread_id:
            message.thread_id = thread_id

        message.save()

        # Redirect back to conversation
        redirect_url = f"{reverse('message_list')}?character={message.receiver_character.id}"
        
        if thread_id:
            redirect_url += f"&thread_id={message.thread_id}"

        return redirect(redirect_url)


### POKE System Views --------------------------------------

class PokeListView(BaseViewMixin, LoginRequiredMixin, ListView):
    """List received and sent POKEs"""
    model = Poke
    template_name = 'pokes/poke_list.html'
    context_object_name = 'pokes'
    paginate_by = 50
    current_page = 'pokes'
    
    def get_queryset(self):
        user_characters = Character.objects.filter(user=self.request.user)
        status_filter = self.request.GET.get('status', 'all')
        
        # Get received POKEs
        received_pokes = Poke.objects.filter(
            receiver_character__in=user_characters
        ).select_related('sender_character', 'sender_character__game', 'sender_character__user')
        
        # Get sent POKEs
        sent_pokes = Poke.objects.filter(
            sender_character__in=user_characters
        ).select_related('receiver_character', 'receiver_character__game', 'receiver_character__user')
        
        # Filter by status
        if status_filter == 'received':
            queryset = received_pokes
        elif status_filter == 'sent':
            queryset = sent_pokes
        elif status_filter == 'pending':
            queryset = received_pokes.filter(status='PENDING')
        else:
            # Combine both, prioritizing received
            queryset = received_pokes.union(sent_pokes, all=True)
        
        return queryset.order_by('-sent_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_characters = Character.objects.filter(user=self.request.user)
        
        # Count unread POKEs
        unread_count = Poke.objects.filter(
            receiver_character__in=user_characters,
            is_read=False,
            status='PENDING'
        ).count()
        
        context['unread_count'] = unread_count
        context['status_filter'] = self.request.GET.get('status', 'all')
        context['title'] = _('POKEs')
        context['content_template'] = 'pokes/poke_list_content.html'
        return context


class SendPokeView(BaseViewMixin, LoginRequiredMixin, FormView):
    """Send POKE to a character"""
    template_name = 'pokes/send_poke.html'
    form_class = PokeForm
    success_url = reverse_lazy('poke_list')
    current_page = 'pokes'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        
        # Get receiver character from URL
        character_id = self.request.GET.get('character')
        if character_id:
            try:
                receiver_character = Character.objects.get(id=character_id)
                if not kwargs.get('initial'):
                    kwargs['initial'] = {}
                kwargs['initial']['receiver_character'] = receiver_character
            except Character.DoesNotExist:
                pass
        
        # Get sender character from URL or use first matching
        sender_character_id = self.request.GET.get('sender_character')
        if sender_character_id:
            try:
                sender_character = Character.objects.get(id=sender_character_id, user=self.request.user)
                kwargs['sender_character'] = sender_character
            except Character.DoesNotExist:
                pass
        
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character_id = self.request.GET.get('character')
        if character_id:
            try:
                context['receiver_character'] = Character.objects.get(id=character_id)
            except Character.DoesNotExist:
                pass
        
        # Get user's characters for selection
        context['user_characters'] = Character.objects.filter(user=self.request.user)
        
        # Check rate limits
        from django.utils import timezone
        from datetime import timedelta
        from django.conf import settings
        yesterday = timezone.now() - timedelta(days=1)
        today_poke_count = Poke.objects.filter(
            sender_character__user=self.request.user,
            sent_date__gte=yesterday
        ).count()
        max_per_day = getattr(settings, 'POKE_MAX_PER_USER_PER_DAY', 5)
        context['pokes_remaining'] = max(0, max_per_day - today_poke_count)
        context['max_per_day'] = max_per_day
        
        return context
    
    def form_valid(self, form):
        poke = form.save()
        messages.success(self.request, _("POKE sent successfully!"))
        return redirect('poke_list')


class PokeDetailView(BaseViewMixin, LoginRequiredMixin, DetailView):
    """View POKE details"""
    model = Poke
    template_name = 'pokes/poke_detail.html'
    context_object_name = 'poke'
    pk_url_kwarg = 'poke_id'
    current_page = 'pokes'
    
    def get_queryset(self):
        user_characters = Character.objects.filter(user=self.request.user)
        return Poke.objects.filter(
            models.Q(sender_character__in=user_characters) |
            models.Q(receiver_character__in=user_characters)
        ).select_related('sender_character', 'receiver_character', 'sender_character__game', 'receiver_character__game')
    
    def get_object(self, queryset=None):
        poke = super().get_object(queryset)
        # Mark as read if user is receiver
        user_characters = Character.objects.filter(user=self.request.user)
        if poke.receiver_character in user_characters and not poke.is_read:
            poke.is_read = True
            from django.utils import timezone
            poke.read_at = timezone.now()
            poke.save(update_fields=['is_read', 'read_at'])
        return poke
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_characters = Character.objects.filter(user=self.request.user)
        poke = self.get_object()
        
        # Check if user can respond (is receiver and status is PENDING)
        context['can_respond'] = (
            poke.receiver_character in user_characters and
            poke.status == 'PENDING'
        )
        
        # Check if user is sender
        context['is_sender'] = poke.sender_character in user_characters
        
        return context


class RespondPokeView(LoginRequiredMixin, View):
    """Respond to POKE by sending POKE back"""
    def post(self, request, poke_id):
        poke = get_object_or_404(
            Poke.objects.select_related('sender_character', 'receiver_character'),
            id=poke_id
        )
        
        # Verify user is receiver
        user_characters = Character.objects.filter(user=request.user)
        if poke.receiver_character not in user_characters:
            raise PermissionDenied("You can only respond to POKEs sent to your characters")
        
        if poke.status != 'PENDING':
            messages.error(request, _("This POKE has already been handled."))
            return redirect('poke_detail', poke_id=poke_id)
        
        # Create response POKE
        try:
            response_poke = Poke.objects.create(
                sender_character=poke.receiver_character,
                receiver_character=poke.sender_character,
                content=_("Hello! I received your POKE."),  # Default response, can be customized later
                status='RESPONDED'
            )
            
            # Mark original POKE as responded
            from django.utils import timezone
            poke.status = 'RESPONDED'
            poke.responded_at = timezone.now()
            poke.save(update_fields=['status', 'responded_at'])
            
            messages.success(request, _("POKE sent! You can now send full messages."))
        except IntegrityError:
            messages.error(request, _("You have already sent a POKE to this character."))
        
        return redirect('poke_list')


class IgnorePokeView(LoginRequiredMixin, View):
    """Ignore a POKE"""
    def post(self, request, poke_id):
        poke = get_object_or_404(Poke, id=poke_id)
        
        # Verify user is receiver
        user_characters = Character.objects.filter(user=request.user)
        if poke.receiver_character not in user_characters:
            raise PermissionDenied("You can only ignore POKEs sent to your characters")
        
        if poke.status != 'PENDING':
            messages.error(request, _("This POKE has already been handled."))
            return redirect('poke_detail', poke_id=poke_id)
        
        poke.status = 'IGNORED'
        poke.save(update_fields=['status'])
        messages.info(request, _("POKE ignored."))
        
        return redirect('poke_list')


class BlockPokeView(LoginRequiredMixin, View):
    """Block a sender and optionally report as spam"""
    def post(self, request, poke_id):
        poke = get_object_or_404(
            Poke.objects.select_related('sender_character', 'receiver_character'),
            id=poke_id
        )
        
        # Verify user is receiver
        user_characters = Character.objects.filter(user=request.user)
        if poke.receiver_character not in user_characters:
            raise PermissionDenied("You can only block POKEs sent to your characters")
        
        # Create block
        PokeBlock.objects.get_or_create(
            blocker_character=poke.receiver_character,
            blocked_character=poke.sender_character,
            defaults={'reason': request.POST.get('reason', '')}
        )
        
        # Mark POKE as blocked and optionally report as spam
        poke.status = 'BLOCKED'
        if request.POST.get('report_spam') == 'on':
            poke.reported_as_spam = True
            poke.reported_by = request.user
            from django.utils import timezone
            poke.reported_at = timezone.now()
        
        poke.save()
        
        messages.success(request, _("Sender blocked. You will not receive more POKEs from this character."))
        return redirect('poke_list')


class BlockCharacterView(LoginRequiredMixin, View):
    """Block a character from all interactions"""
    
    def post(self, request, *args, **kwargs):
        character_id = request.POST.get('character_id')
        reason = request.POST.get('reason', '')
        report_spam = request.POST.get('report_spam') == 'on'
        
        try:
            character_to_block = get_object_or_404(Character, id=character_id)
            user_characters = Character.objects.filter(user=request.user)
            
            # Cannot block own character
            if character_to_block.user == request.user:
                messages.error(request, _("You cannot block your own character."))
                return redirect(request.META.get('HTTP_REFERER', 'character_list'))
            
            # Find which of user's characters should block
            blocking_character_id = request.POST.get('blocking_character_id')
            if blocking_character_id:
                blocking_character = get_object_or_404(
                    Character,
                    id=blocking_character_id,
                    user=request.user
                )
            else:
                # Default: block from character in same game
                blocking_character = user_characters.filter(
                    game=character_to_block.game
                ).first()
                
                # If no character in same game, use first character
                if not blocking_character:
                    blocking_character = user_characters.first()
            
            if not blocking_character:
                messages.error(request, _("You need a character to block from."))
                return redirect(request.META.get('HTTP_REFERER', 'character_list'))
            
            # Create block
            from django.utils import timezone
            block, created = CharacterBlock.objects.get_or_create(
                blocker_character=blocking_character,
                blocked_character=character_to_block,
                defaults={
                    'reason': reason,
                    'reported_as_spam': report_spam,
                    'reported_at': timezone.now() if report_spam else None
                }
            )
            
            if created:
                messages.success(request, _("Character blocked successfully."))
            else:
                messages.info(request, _("Character was already blocked."))
            
            return redirect(request.META.get('HTTP_REFERER', 'character_list'))
            
        except Exception as e:
            messages.error(request, _("Failed to block character: {error}").format(error=str(e)))
            return redirect('character_list')


class UnblockCharacterView(LoginRequiredMixin, View):
    """Unblock a previously blocked character"""
    
    def post(self, request, *args, **kwargs):
        block_id = request.POST.get('block_id')
        character_id = request.POST.get('character_id')
        
        try:
            if block_id:
                block = get_object_or_404(
                    CharacterBlock,
                    id=block_id,
                    blocker_character__user=request.user
                )
                block.delete()
            elif character_id:
                # Unblock by character ID
                user_characters = Character.objects.filter(user=request.user)
                CharacterBlock.objects.filter(
                    blocker_character__in=user_characters,
                    blocked_character_id=character_id
                ).delete()
            
            messages.success(request, _("Character unblocked successfully."))
            return redirect('blocked_characters_list')
            
        except Exception as e:
            messages.error(request, _("Failed to unblock character: {error}").format(error=str(e)))
            return redirect('blocked_characters_list')


class BlockedCharactersListView(LoginRequiredMixin, ListView):
    """List all characters blocked by current user's characters"""
    model = CharacterBlock
    template_name = 'characters/blocked_list.html'
    context_object_name = 'blocks'
    paginate_by = 20
    current_page = 'characters'
    
    def get_queryset(self):
        user_characters = Character.objects.filter(user=self.request.user)
        return CharacterBlock.objects.filter(
            blocker_character__in=user_characters
        ).select_related(
            'blocker_character',
            'blocker_character__game',
            'blocked_character',
            'blocked_character__game',
            'blocked_character__user'
        ).order_by('-blocked_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Blocked Characters')
        context['back_url'] = reverse('account_profile')
        context['back_label'] = _('Back to Profile')
        context['content_template'] = 'characters/blocked_list_content.html'
        return context


@login_required
def propose_game(request):
    if request.method == 'POST':
        form = ProposedGameForm(request.POST)
        if form.is_valid():
            proposed_game = form.save(commit=False)
            proposed_game.created_by = request.user
            proposed_game.save()
            messages.success(request, _("Your game proposal has been submitted successfully!"))
            return redirect('proposed_games_list')
    else:
        form = ProposedGameForm()

    context = {
        'form': form,
        'title': _('Propose a New Game'),
        'content_template': 'games/propose_game_content.html',
        'back_url': reverse('game_list'),
        'back_label': _('Back to Games')
    }
    return render(request, 'games/propose_game.html', context)

def proposed_games_list(request):
    proposed_games = ProposedGame.objects.all().order_by('-votes').prefetch_related('vote_set')
    context = {
        'proposed_games': proposed_games,
        'title': _('Proposed Games'),
        'content_template': 'games/proposed_games_list_content.html',
        'back_url': reverse('game_list'),
        'back_label': _('Back to Games'),
        'show_action': True,
        'action_url': reverse('propose_game'),
        'action_label': _('Propose New Game')
    }
    return render(request, 'games/proposed_games_list.html', context)

@login_required
def vote_for_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    action = request.POST.get('action', 'vote')

    if action == 'vote':
        if game.add_vote(request.user):
            messages.success(request, _("Your vote has been counted!"))
        else:
            messages.error(request, _("You have already voted for this game!"))
    elif action == 'unvote':
        if game.remove_vote(request.user):
            messages.success(request, _("Your vote has been removed!"))
        else:
            messages.error(request, _("You haven't voted for this game!"))

    return HttpResponseRedirect(reverse('proposed_games_list'))

def check_approved_games():
    threshold = 10  # Można zmienić na dynamiczny próg
    proposed_games = ProposedGame.objects.filter(is_approved=False)
    for game in proposed_games:
        if game.votes >= threshold:
            game.is_approved = True
            game.save()
            # Tutaj można dodać logikę do przeniesienia gry do listy gier

### Identity Reveal Views ---------------------------------

class RevealIdentityView(LoginRequiredMixin, View):
    """Reveal user identity to another character"""
    
    def post(self, request, *args, **kwargs):
        sender_character_id = request.POST.get('sender_character')
        receiver_character_id = request.POST.get('receiver_character')
        
        if not sender_character_id or not receiver_character_id:
            messages.error(request, _("Missing required parameters."))
            return redirect('message_list')
        
        try:
            sender_character = get_object_or_404(
                Character,
                id=sender_character_id,
                user=request.user
            )
            receiver_character = get_object_or_404(Character, id=receiver_character_id)
            
            # Create or update identity reveal
            identity_reveal, created = CharacterIdentityReveal.objects.get_or_create(
                revealing_character=sender_character,
                revealed_to_character=receiver_character,
                defaults={'is_active': True}
            )
            
            if not created:
                # Reactivate if it was previously revoked
                identity_reveal.is_active = True
                identity_reveal.revoked_at = None
                identity_reveal.save()
            
            messages.success(
                request,
                _("You're now unmasked to {character_name}! ⭐").format(
                    character_name=receiver_character.nickname
                )
            )
            
        except Exception as e:
            messages.error(request, _("Failed to reveal identity: {error}").format(error=str(e)))
        
        # Redirect back to conversation
        redirect_url = f"{reverse('message_list')}?character={receiver_character_id}"
        if sender_character_id:
            redirect_url += f"&sender={sender_character_id}"
        return redirect(redirect_url)

class HideIdentityView(LoginRequiredMixin, View):
    """Hide (revoke) user identity from another character"""
    
    def post(self, request, *args, **kwargs):
        sender_character_id = request.POST.get('sender_character')
        receiver_character_id = request.POST.get('receiver_character')
        
        if not sender_character_id or not receiver_character_id:
            messages.error(request, _("Missing required parameters."))
            return redirect('message_list')
        
        try:
            sender_character = get_object_or_404(
                Character,
                id=sender_character_id,
                user=request.user
            )
            receiver_character = get_object_or_404(Character, id=receiver_character_id)
            
            # Find and revoke identity reveal
            identity_reveal = CharacterIdentityReveal.objects.filter(
                revealing_character=sender_character,
                revealed_to_character=receiver_character
            ).first()
            
            if identity_reveal:
                identity_reveal.revoke()
                messages.success(
                    request,
                    _("You're now incognito to {character_name} 🎭").format(
                        character_name=receiver_character.nickname
                    )
                )
            else:
                messages.warning(request, _("Identity was not revealed to this character."))
            
        except Exception as e:
            messages.error(request, _("Failed to hide identity: {error}").format(error=str(e)))
        
        # Redirect back to conversation
        redirect_url = f"{reverse('message_list')}?character={receiver_character_id}"
        if sender_character_id:
            redirect_url += f"&sender={sender_character_id}"
        return redirect(redirect_url)
