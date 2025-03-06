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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    description = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])
    year_started = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2099),
        ],
        help_text="Started year in format YYYY.",
    )
    year_ended = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2099),
        ],
        help_text="Ended year in format YYYY.",
    )

    def __str__(self):
        return f"{self.user.username} - {self.nickname} in {self.game.name}"

    def get_games_info(self):
        year_info = ""
        if self.year_started:
            if self.year_ended:
                year_info = f"{self.year_started}-{self.year_ended}"
            else:
                year_info = f"{self.year_started}-present"
        return [{'game': self.game, 'year_info': year_info}]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        # Zapewnia, że kombinacja (user, nickname, game) jest unikalna
        unique_together = ('user', 'nickname', 'game')

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
    sender_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='sent_messages', null=True)
    receiver_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='received_messages', null=True)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    thread_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.sender_character.nickname} -> {self.receiver_character.nickname} ({self.sent_date})"

    class Meta:
        ordering = ['sent_date']  # chronologiczne sortowanie wiadomości

class EmailNotification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
