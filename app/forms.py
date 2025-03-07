from django import forms
from django_registration.forms import RegistrationForm
from .models import Character, Game, CustomUser, Message, ProposedGame
from django.contrib.auth import get_user_model
from django.db import models

class AddCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['nickname', 'game', 'description', 'year_started', 'year_ended', 'avatar']

    nickname = forms.CharField(label='Character Nickname', max_length=100)
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        label='Game',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Brief description of your character (optional)'
        }),
        required=False
    )
    avatar = forms.ImageField(
        label='Character Avatar',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload your character avatar (optional)'
    )
    year_started = forms.IntegerField(
        label='Year started',
        required=False,
        min_value=1900,
        max_value=2099,
        widget=forms.NumberInput(attrs={'placeholder': 'YYYY'})
    )
    year_ended = forms.IntegerField(
        label='Year ended',
        required=False,
        min_value=1900,
        max_value=2099,
        widget=forms.NumberInput(attrs={'placeholder': 'YYYY'})
    )

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
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        empty_label='All Games',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    year = forms.IntegerField(
        min_value=1900,
        max_value=2100,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': '2000'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Upewnij się, że nie modyfikujemy struktury krotek w choices
        self.game_slugs = {str(game.id): game.slug for game in Game.objects.all()}

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'icon', 'desc']

class MessageForm(forms.ModelForm):
    receiver_character = forms.ModelChoiceField(
        queryset=Character.objects.all(),
        required=True,
        label='Character Recipient'
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Type your message...',
            'class': 'form-control chat-input'
        }),
        label=''
    )

    class Meta:
        model = Message
        fields = ['content', 'receiver_character']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        sender_character = kwargs.pop('sender_character', None)
        super(MessageForm, self).__init__(*args, **kwargs)

        if sender_character:
            # Exclude sender's character and characters belonging to the same user
            self.fields['receiver_character'].queryset = Character.objects.exclude(
                models.Q(id=sender_character.id) |
                models.Q(user=sender_character.user)
            )

    def clean(self):
        cleaned_data = super().clean()
        receiver_character = cleaned_data.get('receiver_character')

        if not receiver_character:
            raise forms.ValidationError("Please select a character recipient.")

        return cleaned_data

class ProposedGameForm(forms.ModelForm):
    class Meta:
        model = ProposedGame
        fields = ['name', 'description']
