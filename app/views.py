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

from .forms import AddCharacterForm, CharacterFilterForm, UserEditForm, GameForm, CustomRegistrationForm, UserForm, MessageForm
from .models import Game, Character, Message, CustomUser, GameCategory




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
		print(f"User fields: {dir(user)}")  # Debug line
		print(f"Is CustomUser: {isinstance(user, CustomUser)}")  # Debug line
		print(f"User model: {User}")  # Debug line
		print(f"Has birthday: {'birthday' in dir(user)}")  # Debug line
		print(f"Birthday value: {getattr(user, 'birthday', None)}")  # Debug line

		characters = Character.objects.filter(user=user)

		initial_data = {
			'first_name': user.first_name,
			'last_name': user.last_name,
			'birthday': getattr(user, 'birthday', None),
			'facebook': getattr(user, 'facebook', ''),
			'twitch': getattr(user, 'twitch', ''),
			'gender': getattr(user, 'gender', ''),
		}
		form = UserEditForm(instance=user, initial=initial_data)
		context = {
			'user': user,
			'characters': characters,
			'form': form,
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

class AddCharacterView(LoginRequiredMixin, CreateView):
	model = Character
	form_class = AddCharacterForm
	template_name = 'characters/add_character.html'
	success_url = reverse_lazy('character_list')

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			character = form.save(commit=False)
			character.user = request.user
			character.save()
			return redirect(self.success_url)
		return render(request, self.template_name, {'form': form})


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
					Q(year_started__lte=year) & (Q(year_ended__gte=year) | Q(year_ended__isnull=True))
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

		if game_slug:
			try:
				# Znajdź grę na podstawie sluga i ustaw jej ID jako początkową wartość dla pola 'game'.
				game = Game.objects.get(slug=game_slug)
				initial_data = {'game': game.id}
				context['form'] = CharacterFilterForm(initial=initial_data)
			except Game.DoesNotExist:
				# Jeśli gra o danym slugu nie istnieje, użyj pustego formularza.
				context['form'] = CharacterFilterForm()
		else:
			context['form'] = CharacterFilterForm()

		return context


class CharacterView(BaseViewMixin, DetailView):
	current_page = 'characters'
	model = Character
	template_name = 'characters/character_detail.html'
	context_object_name = 'character'
	slug_url_kwarg = 'nickname'
	slug_field = 'nickname'

	def get_object(self, queryset=None):
		user = self.kwargs['user']
		nickname = self.kwargs['nickname']
		return get_object_or_404(Character, user__username=user, nickname=nickname)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		character = self.get_object()
		context['title'] = character.nickname
		context['content_template'] = 'characters/character_detail_content.html'
		return context

class CharacterEditView(BaseViewMixin, LoginRequiredMixin, UpdateView):
	current_page = 'characters'
	template_name = 'characters/add_character.html'
	model = Character
	form_class = AddCharacterForm

	def get_object(self):
		user = self.kwargs['user']
		nickname = self.kwargs['nickname']
		return get_object_or_404(Character, user__username=user, nickname=nickname)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.form_class(request.POST, request.FILES, instance=self.object)
		if form.is_valid():
			form.save()
			return redirect(self.get_success_url())
		return render(request, self.template_name, {'form': form})

	def get_success_url(self):
		return reverse('character_detail', kwargs={
			'user': self.object.user.username,
			'nickname': self.object.nickname
		})



### Games- --------------------------------------------

class GameListView(BaseViewMixin, ListView):
	current_page = 'games'
	model = Game
	template_name = 'games/games_list.html'
	context_object_name = 'games'

class GameDetailView(BaseViewMixin, DetailView):
	current_page = 'games'
	model = Game
	template_name = 'games/game_detail.html'
	context_object_name = 'game'
	slug_field = 'slug'
	slug_url_kwarg = 'slug'

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
		context['action'] = 'edit'
		return context

class GameDeleteView(BaseViewMixin, DeleteView):
	current_page = 'games'
	model = Game
	template_name = 'games/game_confirm_delete.html'
	success_url = '/games/'  # URL to redirect after successful deletion

	def delete(self, request, *args, **kwargs):
		game = self.get_object()
		messages.success(request, f'The game "{game.name}" has been deleted successfully.')
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
            return Message.objects.filter(thread_id=thread_id)
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
                    return Message.objects.filter(thread_id=existing_thread)
                else:
                    return Message.objects.none()
            except Character.DoesNotExist:
                return Message.objects.none()
        else:
            # Pobierz wszystkie wiadomości dla wszystkich postaci użytkownika
            return Message.objects.filter(
                models.Q(sender_character__in=user_characters) |
                models.Q(receiver_character__in=user_characters)
            ).order_by('-sent_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver_character_id = self.request.GET.get('character')
        thread_id = self.request.GET.get('thread_id')
        user_characters = Character.objects.filter(user=self.request.user)

        if not user_characters.exists():
            context['error_message'] = "You need to create a character first to send messages."
            return context

        if receiver_character_id:
            try:
                receiver_character = Character.objects.get(id=receiver_character_id)
                context['receiver_character'] = receiver_character
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

class UserCharactersListView(ListView):
    model = Character
    template_name = 'characters/user_characters_list.html'

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

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

        # Przekieruj z powrotem do konwersacji
        if thread_id:
            return redirect(f'{reverse("message_list")}?thread_id={message.thread_id}')
        else:
            return redirect(f'{reverse("message_list")}?character={message.receiver_character.id}')
