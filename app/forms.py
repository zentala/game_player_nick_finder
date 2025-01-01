from django import forms
from django.forms import inlineformset_factory
from django_registration.forms import RegistrationForm
from .models import Character, Game, GamePlayed, CustomUser
from django.contrib.auth import get_user_model

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

class UserForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Twoja nazwa użytkownika"
        self.fields['email'].help_text = "Podaj swój adres e-mail"

    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = RegistrationForm.Meta.fields

class CustomRegistrationForm(RegistrationForm):
    birthday = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    facebook = forms.URLField(required=False)
    twitch = forms.URLField(required=False)
    gender = forms.ChoiceField(
        choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')],
        required=False,
        widget=forms.Select(choices=[('', '---------'), ('MALE', 'MALE'), ('FEMALE', 'FEMALE')])
    )

    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = RegistrationForm.Meta.fields + ['birthday', 'facebook', 'twitch', 'gender']

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    birthday = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    facebook = forms.URLField(required=False)
    twitch = forms.URLField(required=False)
    gender = forms.ChoiceField(
        choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')],
        required=False,
        widget=forms.Select(choices=[('', '---------'), ('MALE', 'MALE'), ('FEMALE', 'FEMALE')])
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'birthday', 'facebook', 'twitch', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class CharacterFilterForm(forms.Form):
    nickname = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': ''}))
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
