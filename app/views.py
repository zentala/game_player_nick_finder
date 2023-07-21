# # game_player_nick_finder/app/views.py
# from django.shortcuts import render
# from .models import YourModel

# def your_view(request):
#     # Dodaj logikę widoku
#     objects = YourModel.objects.all()
#     return render(request, 'app/index.html', {'objects': objects})

import json
from django.shortcuts import render

def index(request):
    # Pobierz dane z pliku JSON
    with open('example_data.json', 'r') as json_file:
        data = json.load(json_file)

    context = {'data': data}    

    return render(request, 'app/index.html', context)
