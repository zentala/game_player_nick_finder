from django import forms
from django_registration.forms import RegistrationForm
from .models import (
    Character, Game, CustomUser, Message, ProposedGame,
    CharacterFriendRequest, CharacterProfile
)
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
    PROFILE_VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('FRIENDS_ONLY', 'Friends Only'),
        ('PRIVATE', 'Private'),
    ]
    
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
    
    # Profile fields
    profile_visibility = forms.ChoiceField(
        choices=PROFILE_VISIBILITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    steam_profile = forms.URLField(required=False)
    youtube_channel = forms.URLField(required=False)
    stackoverflow_profile = forms.URLField(required=False)
    github_profile = forms.URLField(required=False)
    linkedin_profile = forms.URLField(required=False)
    profile_bio = forms.CharField(
        required=False,
        max_length=1000,
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'})
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'birthday', 'facebook', 'twitch', 'gender',
            'profile_visibility', 'steam_profile', 'youtube_channel',
            'stackoverflow_profile', 'github_profile', 'linkedin_profile',
            'profile_bio', 'profile_picture'
        ]

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
    PRIVACY_MODES = [
        ('ANONYMOUS', 'Hide my identity (Character only)'),
        ('REVEAL_IDENTITY', 'Show my identity (Character + Username)'),
    ]
    
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
    
    privacy_mode = forms.ChoiceField(
        choices=PRIVACY_MODES,
        initial='ANONYMOUS',
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Privacy Mode',
        help_text='Choose whether to reveal your user identity'
    )

    class Meta:
        model = Message
        fields = ['content', 'receiver_character', 'privacy_mode']

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
        privacy_mode = cleaned_data.get('privacy_mode', 'ANONYMOUS')

        if not receiver_character:
            raise forms.ValidationError("Please select a character recipient.")
        
        # Set identity_revealed based on privacy_mode
        cleaned_data['identity_revealed'] = (privacy_mode == 'REVEAL_IDENTITY')

        return cleaned_data
    
    def save(self, commit=True):
        message = super().save(commit=False)
        privacy_mode = self.cleaned_data.get('privacy_mode', 'ANONYMOUS')
        message.privacy_mode = privacy_mode
        message.identity_revealed = (privacy_mode == 'REVEAL_IDENTITY')
        
        if commit:
            message.save()
        return message

class ProposedGameForm(forms.ModelForm):
    class Meta:
        model = ProposedGame
        fields = ['name', 'description']


class CharacterFriendRequestForm(forms.ModelForm):
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Optional message...',
            'class': 'form-control'
        }),
        label='Message (optional)'
    )
    
    class Meta:
        model = CharacterFriendRequest
        fields = ['message']


class CharacterProfileForm(forms.ModelForm):
    custom_bio = forms.CharField(
        required=False,
        max_length=2000,
        widget=forms.Textarea(attrs={
            'rows': 6,
            'class': 'form-control',
            'placeholder': 'Tell your gaming story...'
        }),
        label='Custom Bio'
    )
    
    is_public = forms.BooleanField(
        required=False,
        initial=True,
        label='Public Profile',
        help_text='Make this profile visible to everyone'
    )
    
    class Meta:
        model = CharacterProfile
        fields = ['custom_bio', 'is_public']
