# # game_player_nick_finder/app/views.py
# from django.shortcuts import render
# from .models import YourModel

# def your_view(request):
#     # Dodaj logikę widoku
#     objects = YourModel.objects.all()
#     return render(request, 'app/index.html', {'objects': objects})

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import AddGameAndCharacterForm
from .models import Game, Character

def index(request):
    # Pobierz dane z pliku JSON
    with open('example_data.json', 'r') as json_file:
        data = json.load(json_file)

    context = {'data': data}    

    return render(request, 'index.html', context)

@login_required
def welcome(request):
    # Twój kod widoku
    pass

@login_required
def account_profile(request):
    if request.user.is_authenticated:
        print("User is authenticated.")
        print("Username:", request.user.username)
    else:
        print("User is not authenticated.")

    if hasattr(request.user, 'account'):
        account = request.user.account
        characters = Character.objects.filter(user=account)
        return render(request, 'account_profile.html', {'user': request.user, 'characters': characters})
    else:
        return render(request, 'account_profile.html', {'user': request.user})


# @login_required
# def registration_logout(request):
#     # Kod do obsługi wylogowania użytkownika
#     # ...
#     return render(request, 'registration/logout.html')

def add_game_and_character(request):
    if request.method == 'POST':
        form = AddGameAndCharacterForm(request.POST)
        if form.is_valid():
            # Pobierz dane z formularza
            game_name = form.cleaned_data['game_name']
            game_icon = form.cleaned_data['game_icon']
            character_nickname = form.cleaned_data['character_nickname']
            date_range_start = form.cleaned_data['date_range_start']
            date_range_end = form.cleaned_data['date_range_end']
            description = form.cleaned_data['description']
            visibility = form.cleaned_data['visibility']

            # Zapisz dane do bazy danych
            game = Game.objects.create(name=game_name, icon=game_icon)
            character = Character.objects.create(user=request.user, nickname=character_nickname, game=game,
                                                 date_range_start=date_range_start, date_range_end=date_range_end,
                                                 description=description, visibility=visibility)

            return redirect('profile')  # Przekierowanie na stronę profilu użytkownika po dodaniu danych

    else:
        form = AddGameAndCharacterForm()

    return render(request, 'add_game_and_character.html', {'form': form})