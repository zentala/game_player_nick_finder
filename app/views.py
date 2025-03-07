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
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from .forms import AddCharacterForm, CharacterFilterForm, UserEditForm, GameForm, CustomRegistrationForm, UserForm, MessageForm, ProposedGameForm
from .models import Game, Character, Message, CustomUser, GameCategory, ProposedGame, Vote




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

class IndexView(BaseViewMixin, TemplateView):
	current_page = 'home'
	template_name = 'index.html'

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
		form = UserEditForm(request.POST, instance=user)

		if form.is_valid():
			user = form.save()
			messages.success(request, 'Profile updated successfully!')
			return redirect('account_profile')

		context = {
			'user': user,
			'characters': characters,
			'form': form,
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

		# Dodaj mapowanie ID gier do ich slugów
		context['game_slugs_json'] = {str(g.id): g.slug for g in Game.objects.all()}

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

		if self.request.user == character.user:
			context['show_action'] = True
			context['action_url'] = reverse('character_edit', kwargs={
				'nickname': character.nickname,
				'hash_id': character.hash_id
			})
			context['action_label'] = _('Edit Character')

		return context

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
            # Zamiast wszystkich wiadomości, zwróć tylko najnowsze z każdej konwersacji
            conversations = []

            # Pobierz unikalne pary rozmówców
            pairs = set()
            user_character_ids = list(user_characters.values_list('id', flat=True))

            # Pobierz wszystkie wiadomości gdzie użytkownik jest nadawcą lub odbiorcą
            all_messages = Message.objects.filter(
                models.Q(sender_character__in=user_characters) |
                models.Q(receiver_character__in=user_characters)
            ).select_related('sender_character', 'receiver_character', 'sender_character__game', 'receiver_character__game')

            # Grupuj wiadomości według par rozmówców
            for message in all_messages:
                # Upewnij się, że pierwszy element pary to zawsze postać użytkownika
                if message.sender_character.id in user_character_ids:
                    pair = (message.sender_character.id, message.receiver_character.id)
                else:
                    pair = (message.receiver_character.id, message.sender_character.id)

                # Dodaj parę do zbioru jeśli jeszcze jej nie ma
                if pair not in pairs:
                    pairs.add(pair)
                    # Znajdź najnowszą wiadomość dla tej pary
                    latest_message = Message.objects.filter(
                        models.Q(
                            sender_character=Character.objects.get(id=pair[0]),
                            receiver_character=Character.objects.get(id=pair[1])
                        ) | models.Q(
                            sender_character=Character.objects.get(id=pair[1]),
                            receiver_character=Character.objects.get(id=pair[0])
                        )
                    ).order_by('-sent_date').first()

                    if latest_message:
                        conversations.append(latest_message)

            # Posortuj konwersacje według daty ostatniej wiadomości (najnowsze na górze)
            return sorted(conversations, key=lambda m: m.sent_date, reverse=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver_character_id = self.request.GET.get('character')
        sender_character_id = self.request.GET.get('sender')
        thread_id = self.request.GET.get('thread_id')
        user_characters = Character.objects.filter(user=self.request.user)

        if not user_characters.exists():
            context['error_message'] = _("You need to create a character first to send messages.")
            return context

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
                    context['sender_character'] = matching_characters.first()
                elif sender_character_id and matching_characters.filter(id=sender_character_id).exists():
                    # Jeśli wybrano konkretną postać do wysyłania
                    context['sender_character'] = matching_characters.get(id=sender_character_id)

                context['form'] = MessageForm(
                    user=self.request.user,
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
        form = MessageForm(request.POST, user=request.user)

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

        message.sender_character = matching_character
        thread_id = self.request.GET.get('thread_id')

        if thread_id:
            message.thread_id = thread_id

        message.save()

        # Przekieruj z powrotem do konwersacji z zachowaniem informacji o nadawcy
        if sender_character_id:
            redirect_url = f"{reverse('message_list')}?character={message.receiver_character.id}&sender={sender_character_id}"
        else:
            redirect_url = f"{reverse('message_list')}?character={message.receiver_character.id}"

        if thread_id:
            redirect_url += f"&thread_id={message.thread_id}"

        return redirect(redirect_url)

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
