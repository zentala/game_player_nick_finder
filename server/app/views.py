from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django_registration.backends.one_step.views import RegistrationView

from .forms import AddCharacterForm, CharacterFilterForm, UserEditForm, GameForm, GamePlayedFormSet, CustomRegistrationForm
from .models import Game, Character, GamePlayed




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
class BaseViewMixin:
    current_page = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = self.current_page
        return context

class IndexView(BaseViewMixin, TemplateView):
    current_page = 'home'
    template_name = 'index.html'

class AccountProfileView(LoginRequiredMixin, View):
    template_name = 'profile'
    template_name = 'account_profile.html'

    def get(self, request):
        user = request.user
        characters = Character.objects.filter(user=user)
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = UserEditForm(instance=user.account, initial=initial_data)
        context = {
            'user': user,
            'characters': characters,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        characters = Character.objects.filter(user=user)
        form = UserEditForm(request.POST, instance=user.account)

        if form.is_valid():
            form.save()
            # Get the updated first name and last name from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            # Update the user's first name and last name
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect('account_profile')

        # If the form is not valid, render the template with the form and other context data
        context = {
            'user': user,
            'characters': characters,
            'form': form,
        }
        return render(request, self.template_name, context)



### Characters ----------------------------------------

class AddCharacterView(LoginRequiredMixin, BaseViewMixin, CreateView):
    current_page = 'characters'
    template_name = 'characters/add_character.html'
    form_class = AddCharacterForm

    def get(self, request):
        form = self.form_class(initial={'visibility': True})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            description = form.cleaned_data['description']
            visibility = form.cleaned_data['visibility']
            games = form.cleaned_data['games']

            character = Character.objects.create(user=request.user, nickname=nickname,
                                                 description=description, visibility=visibility)

            for game in games:
                GamePlayed.objects.create(character=character, game=game)

            return redirect('account_profile')

        return render(request, self.template_name, {'form': form})


class CharacterListView(BaseViewMixin, ListView):
    model = Character
    template_name = 'characters/character_list.html'
    current_page = 'characters'
    context_object_name = 'characters'
    paginate_by = 10

    def get_queryset(self):
        form = CharacterFilterForm(self.request.GET)
        if form.is_valid():
            game = form.cleaned_data['game']
            year = form.cleaned_data['year']
            nickname = form.cleaned_data['nickname']
            queryset = Character.objects.all()

            if game:
                queryset = queryset.filter(gameplayed__game=game)
            
            if year is not None:
                queryset = queryset.filter(
                    Q(gameplayed__year_started__lte=year) & (Q(gameplayed__year_ended__gte=year) | Q(gameplayed__year_ended__isnull=True))
                )

            if nickname:  # If nickname is provided, filter the queryset by nickname
                queryset = queryset.filter(nickname__icontains=nickname)
            return queryset
        return Character.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CharacterFilterForm(self.request.GET)
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
    
class CharacterEditView(BaseViewMixin, LoginRequiredMixin, UpdateView):
    current_page = 'characters'
    template_name = 'characters/add_character.html'  # Reuse the add_character.html template

    def get(self, request, user, nickname):
        character = get_object_or_404(Character, user__username=user, nickname=nickname)
        form = AddCharacterForm(instance=character)
        formset = GamePlayedFormSet(instance=character)
        empty_form = GamePlayedFormSet(instance=character).empty_form

        context = {
            'form': form,
            'formset': formset,
            'empty_form': empty_form,
            'edit_mode': True,
        }
        return render(request, self.template_name, context)

    def post(self, request, user, nickname):
        character = get_object_or_404(Character, user__username=user, nickname=nickname)
        form = AddCharacterForm(request.POST, instance=character)
        formset = GamePlayedFormSet(request.POST, instance=character)

        if form.is_valid() and formset.is_valid():
            character = form.save()

            # Save game played instances
            for form in formset:
                game_played = form.save(commit=False)
                game_played.character = character
                game_played.save()

            return redirect(reverse('character_detail', args=[user, nickname]))

        # If the form is not valid, render the template with the form and other context data
        context = {
            'form': form,
            'formset': formset,
            'empty_form': GamePlayedFormSet(instance=character).empty_form,
            'edit_mode': True,
        }
        return render(request, self.template_name, context)



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
