from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import salted_hmac
import uuid

# replace User model with CustomUser
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birthday = models.DateField(null=True, blank=True, default=None)
    facebook = models.URLField(blank=True)
    twitch = models.URLField(blank=True)
    gender = models.CharField(
        max_length=6,
        choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')],
        blank=True
    )

    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change this to avoid conflict
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change this to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            self.password,
            algorithm='sha256',
        ).hexdigest()

    @classmethod
    def get_default_pk(cls):
        return uuid.uuid4()

    def __str__(self):
        return self.username

class GameCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Game(models.Model):
    # slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='icons/', blank=True)
    desc = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])
    category = models.ForeignKey(GameCategory, on_delete=models.CASCADE, related_name='games')
    img = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Character(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE) # related_name='characters'
    nickname = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
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
        return f"{self.user.username} - {self.nickname} in {self.game.name}"


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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='friend_of')

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"

class FriendRequest(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_friend_requests')
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class EmailNotification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
