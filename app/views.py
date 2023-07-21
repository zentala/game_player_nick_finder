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

class AccountProfile(TemplateView):
    template_name = 'account_profile.html'

# @login_required
# def registration_logout(request):
#     # Kod do obsługi wylogowania użytkownika
#     # ...
#     return render(request, 'registration/logout.html')