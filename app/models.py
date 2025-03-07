from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import salted_hmac
import uuid
import random
import string
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import json

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
    STATUS_CHOICES = [
        ('PROPOSED', 'Proposed'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='icons/', blank=True)
    desc = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])
    category = models.ForeignKey(GameCategory, on_delete=models.CASCADE, related_name='games')
    img = models.URLField(blank=True)

    # Nowe pola
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROPOSED')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='proposed_games')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    votes_count = models.IntegerField(default=0)
    votes_required = models.IntegerField(default=10)  # próg głosów potrzebny do publikacji
    tags = models.TextField(blank=True, default='[]')  # Przechowujemy tagi jako JSON

    @property
    def tags_list(self):
        """Zwraca listę tagów"""
        try:
            return json.loads(self.tags)
        except (json.JSONDecodeError, TypeError):
            return []

    @tags_list.setter
    def tags_list(self, value):
        """Ustawia listę tagów"""
        self.tags = json.dumps(list(set(value)))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def add_vote(self, user):
        """Dodaje głos użytkownika"""
        if not self.has_user_voted(user):
            Vote.objects.create(user=user, game=self)
            self.votes_count = Vote.objects.filter(game=self).count()
            if self.votes_count >= self.votes_required and self.status == 'PROPOSED':
                self.status = 'PUBLISHED'
                self.published_at = timezone.now()
            self.save()
            return True
        return False

    def remove_vote(self, user):
        """Usuwa głos użytkownika"""
        vote = Vote.objects.filter(user=user, game=self).first()
        if vote:
            vote.delete()
            self.votes_count = Vote.objects.filter(game=self).count()
            if self.votes_count < self.votes_required and self.status == 'PUBLISHED':
                self.status = 'PROPOSED'
                self.published_at = None
            self.save()
            return True
        return False

    def has_user_voted(self, user):
        """Sprawdza czy użytkownik już głosował"""
        return Vote.objects.filter(user=user, game=self).exists()

    def add_tag(self, tag):
        """Dodaje tag do gry"""
        if isinstance(self.tags, list):
            if tag not in self.tags:
                self.tags.append(tag)
                self.save()
        else:  # dla SQLite
            tags = set(self.tags.split(',')) if self.tags else set()
            tags.add(tag)
            self.tags = ','.join(tags)
            self.save()

class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    hash_id = models.CharField(max_length=10, blank=True, db_index=True, unique=True)
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
        return f"{self.nickname} in {self.game.name}"

    def save(self, *args, **kwargs):
        if not self.hash_id or self.hash_id.strip() == '':
            # Generuj unikalny hash tylko gdy hash_id jest puste
            self.hash_id = self._generate_unique_hash()
        super().save(*args, **kwargs)

    def _generate_unique_hash(self):
        while True:
            # Generowanie losowego 10-znakowego hash'a z małych, dużych liter i cyfr
            chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
            hash_id = ''.join(random.choices(chars, k=10))
            # Sprawdzenie, czy taki hash już istnieje
            if not Character.objects.filter(hash_id=hash_id).exists():
                return hash_id

    def get_absolute_url(self):
        return reverse('character_detail', kwargs={'nickname': self.nickname, 'hash_id': self.hash_id})

    def get_games_info(self):
        year_info = ""
        if self.year_started:
            if self.year_ended:
                year_info = f"{self.year_started}-{self.year_ended}"
            else:
                year_info = f"{self.year_started}-present"
        return [{'game': self.game, 'year_info': year_info}]

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

class ProposedGame(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    votes = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')
