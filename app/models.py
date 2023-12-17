from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class Game(models.Model):
    # slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='icons/', blank=True)
    desc = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Account(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    # games_played = models.ManyToManyField(Game, through='GamePlayed')
    birthday = models.DateField(null=True, blank=True, default=None)
    facebook = models.URLField(blank=True)
    twitch = models.URLField(blank=True)
    gender = models.CharField(
        max_length=6, 
        choices=[('MALE', 'MALE'),('FEMALE', 'FEMALE')]
    )

    def __str__(self):
        return self.user.username

class Character(models.Model):
    # user = models.ForeignKey(Account, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    games = models.ManyToManyField(Game, through='GamePlayed')
    nickname = models.TextField(validators=[MaxLengthValidator(100)])
    description = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])
    visibility = models.BooleanField()

    def get_games_info(self):
        game_info = []
        played_games = GamePlayed.objects.filter(character=self)
        for game in played_games:
            info = {'game': game.game}
            if game.year_started is not None and game.year_ended is not None:
                info['year_info'] = f'{game.year_started}-{game.year_ended}'
            elif game.year_started is not None:
                info['year_info'] = f'{game.year_started}-'
            elif game.year_ended is not None:
                info['year_info'] = f'-{game.year_ended}'
            else:
                info['year_info'] = ''
            game_info.append(info)
        return game_info

    def __str__(self):
        return f"{self.user} - {self.nickname}"
    

class GamePlayed(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    year_started = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),  # Minimalny rok (zmień wartość na odpowiednią)
            MaxValueValidator(2099),  # Maksymalny rok (zmień wartość na odpowiednią)
        ],
        help_text="Started year in format YYYY.",
    )
    year_ended = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),  # Minimalny rok (zmień wartość na odpowiednią)
            MaxValueValidator(2099),  # Maksymalny rok (zmień wartość na odpowiednią)
        ],
        help_text="Ended year in format YYYY.",
    )

    def __str__(self):
        if self.year_ended is None:
            return f"{self.character} - {self.game} - {self.year_started}"
        else:
            return f"{self.character} - {self.game} - {self.year_started} to {self.year_ended}"



class Friend(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friend_of')

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_friend_requests')
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
class EmailNotification(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject