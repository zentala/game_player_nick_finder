from django import forms
from django.forms import inlineformset_factory
from .models import Account, Character, Game, GamePlayed

class AddCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['nickname', 'games', 'description', 'visibility']
    
    nickname = forms.CharField(label='Character Nickname', max_length=100)

    games = forms.ModelMultipleChoiceField(
        queryset=Game.objects.all(),
        label='Games',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False)
    visibility = forms.BooleanField(label='Visibility', required=False)

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Account
        fields = ['birthday', 'facebook', 'twitch', 'gender']

    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    gender = forms.CharField(
        max_length=6,
        widget=forms.Select(choices=[('', '---------'), ('MALE', 'MALE'), ('FEMALE', 'FEMALE')]),
        required=False,  # Pole jest teraz opcjonalne, użytkownik może pozostawić je puste
    )

class CharacterFilterForm(forms.Form):
    nickname = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'ShadowWarrior01'}))
    game = forms.ModelChoiceField(queryset=Game.objects.all(), empty_label='All Games', required=False)
    year = forms.IntegerField(min_value=1900, max_value=2100, required=False, widget=forms.NumberInput(attrs={'placeholder': '2001'}))

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'icon', 'desc']

class GamePlayedForm(forms.ModelForm):
    class Meta:
        model = GamePlayed
        fields = ['game', 'year_started', 'year_ended']

GamePlayedFormSet = inlineformset_factory(Character, GamePlayed, form=GamePlayedForm, extra=0, can_delete=True)
