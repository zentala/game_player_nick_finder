# # game_player_nick_finder/app/views.py
# from django.shortcuts import render
# from .models import YourModel

# def your_view(request):
#     # Dodaj logikę widoku
#     objects = YourModel.objects.all()
#     return render(request, 'app/index.html', {'objects': objects})

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, CreateView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.urls import reverse

from .forms import AddCharacterForm, CharacterFilterForm, UserEditForm, GameForm, GamePlayedFormSet
from .models import Game, Character, GamePlayed

def index(request):
    # Pobierz dane z pliku JSON
    with open('example_data.json', 'r') as json_file:
        data = json.load(json_file)

    context = {'data': data}    

    return render(request, 'index.html', context)


class AccountProfileView(LoginRequiredMixin, View):
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

class AddCharacterView(LoginRequiredMixin, View):
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


class CharacterListView(ListView):
    model = Character
    template_name = 'characters/character_list.html'
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
    
class CharacterView(DetailView):
    model = Character
    template_name = 'characters/character_detail.html'
    context_object_name = 'character'
    slug_url_kwarg = 'nickname'
    slug_field = 'nickname'

    def get_object(self, queryset=None):
        user = self.kwargs['user']
        nickname = self.kwargs['nickname']
        return get_object_or_404(Character, user__username=user, nickname=nickname)
    
class CharacterEditView(LoginRequiredMixin, View):
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
    

class GameListView(ListView):
    model = Game
    template_name = 'games/games_list.html'
    context_object_name = 'games'

class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class GameCreateView(CreateView):
    model = Game
    template_name = 'games/game_form.html'
    form_class = GameForm
    success_url = '/games/'  # URL to redirect after successful form submission

    def form_valid(self, form):
        response = super().form_valid(form)
        # Dodajemy dodatkową logikę po zapisaniu formularza, jeśli to konieczne
        return response