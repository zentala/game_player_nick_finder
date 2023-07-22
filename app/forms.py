from django import forms
from .models import Game, Character

class AddGameAndCharacterForm(forms.Form):
    game_name = forms.CharField(label='Game Name', max_length=100)
    game_icon = forms.ImageField(label='Game Icon')
    character_nickname = forms.CharField(label='Character Nickname', max_length=100)
    date_range_start = forms.DateField(label='Date Range Start')
    date_range_end = forms.DateField(label='Date Range End')
    description = forms.CharField(label='Description', widget=forms.Textarea)
    visibility = forms.BooleanField(label='Visibility', required=False)
