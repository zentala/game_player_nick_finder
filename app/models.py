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
    PROFILE_VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('FRIENDS_ONLY', 'Friends Only'),
        ('PRIVATE', 'Private'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birthday = models.DateField(null=True, blank=True, default=None)
    facebook = models.URLField(blank=True)
    twitch = models.URLField(blank=True)
    gender = models.CharField(
        max_length=6,
        choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')],
        blank=True
    )
    
    # Profile visibility settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=PROFILE_VISIBILITY_CHOICES,
        default='FRIENDS_ONLY',
        help_text='Who can see your profile'
    )
    
    # Social media links
    steam_profile = models.URLField(blank=True)
    youtube_channel = models.URLField(blank=True)
    stackoverflow_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    custom_links = models.JSONField(default=list, blank=True)  # Array of {name, url}
    
    # Profile customization
    profile_bio = models.TextField(blank=True, max_length=1000)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)

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


# Character-based friend system (Epic 2)
class CharacterFriend(models.Model):
    """
    Friendship between two characters (not users)
    """
    character1 = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        related_name='friends_as_character1'
    )
    character2 = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        related_name='friends_as_character2'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('character1', 'character2')
        indexes = [
            models.Index(fields=['character1', 'character2']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure character1.id < character2.id to avoid duplicates
        # We need to compare UUIDs properly
        if str(self.character1.id) > str(self.character2.id):
            self.character1, self.character2 = self.character2, self.character1
        super().save(*args, **kwargs)
    
    def get_other_character(self, character):
        """Get the other character in this friendship"""
        if character == self.character1:
            return self.character2
        return self.character1
    
    def __str__(self):
        return f"{self.character1.nickname} <-> {self.character2.nickname}"


class CharacterFriendRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    ]
    
    sender_character = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'
    )
    receiver_character = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        related_name='received_friend_requests'
    )
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    message = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('sender_character', 'receiver_character')
    
    def __str__(self):
        return f"{self.sender_character.nickname} -> {self.receiver_character.nickname} ({self.status})"

class Message(models.Model):
    PRIVACY_MODES = [
        ('ANONYMOUS', 'Anonymous'),
        ('REVEAL_IDENTITY', 'Reveal Identity'),
    ]
    
    sender_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='sent_messages', null=True)
    receiver_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='received_messages', null=True)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    thread_id = models.UUIDField(default=uuid.uuid4, editable=False)
    privacy_mode = models.CharField(
        max_length=20,
        choices=PRIVACY_MODES,
        default='ANONYMOUS',
        help_text='Privacy mode when message was sent'
    )
    identity_revealed = models.BooleanField(
        default=False,
        help_text='Whether sender revealed their user identity'
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sender_character.nickname} -> {self.receiver_character.nickname} ({self.sent_date})"

    class Meta:
        ordering = ['sent_date']  # chronologiczne sortowanie wiadomości

class CharacterIdentityReveal(models.Model):
    """
    Tracks when a character reveals their identity to another character.
    Once revealed, all future messages in this conversation will show user identity.
    Can be revoked by the revealing character.
    """
    revealing_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='identity_reveals_sent'
    )
    revealed_to_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='identity_reveals_received'
    )
    revealed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text='Whether the identity reveal is currently active')
    revoked_at = models.DateTimeField(null=True, blank=True, help_text='When the identity reveal was revoked')
    
    class Meta:
        unique_together = ('revealing_character', 'revealed_to_character')
        ordering = ['-revealed_at']
    
    def __str__(self):
        status = "Active" if self.is_active else "Revoked"
        return f"{self.revealing_character.nickname} -> {self.revealed_to_character.nickname} ({status})"
    
    def revoke(self):
        """Revoke the identity reveal"""
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save()

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


# Character custom profile (Epic 4)
class CharacterProfile(models.Model):
    character = models.OneToOneField(
        'Character',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Custom content
    custom_bio = models.TextField(blank=True, max_length=2000)
    custom_images = models.JSONField(default=list, blank=True)  # Array of image URLs
    screenshots = models.JSONField(default=list, blank=True)  # Array of screenshot URLs
    memories = models.JSONField(default=list, blank=True)  # Array of memory objects
    
    # Settings
    is_public = models.BooleanField(default=True, help_text='Show profile to everyone')
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.character.nickname}"


# POKE System (Epic 1 Enhancement)
class Poke(models.Model):
    """
    POKE - lightweight, spam-protected initial contact mechanism.
    Users must exchange mutual POKEs before full messaging is unlocked.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),      # Sent, waiting for response
        ('RESPONDED', 'Responded'),  # Recipient sent POKE back
        ('IGNORED', 'Ignored'),      # Recipient ignored
        ('BLOCKED', 'Blocked'),      # Blocked by recipient
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='sent_pokes'
    )
    receiver_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='received_pokes'
    )
    
    # Content (strictly limited)
    content = models.CharField(
        max_length=100,
        help_text='POKE content (max 100 characters, no URLs or links)'
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    sent_date = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Moderation
    reported_as_spam = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    reported_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reported_pokes'
    )
    
    class Meta:
        unique_together = ('sender_character', 'receiver_character')
        ordering = ['-sent_date']
        indexes = [
            models.Index(fields=['receiver_character', 'status', '-sent_date']),
            models.Index(fields=['sender_character', 'status']),
        ]
    
    def can_send_full_message(self):
        """Check if mutual POKE exchange completed"""
        return self.status == 'RESPONDED' or self.is_mutual()
    
    def is_mutual(self):
        """Check if receiver also sent a POKE back"""
        return Poke.objects.filter(
            sender_character=self.receiver_character,
            receiver_character=self.sender_character,
            status__in=['PENDING', 'RESPONDED']
        ).exists()
    
    def __str__(self):
        return f"{self.sender_character.nickname} -> {self.receiver_character.nickname} ({self.status})"


class PokeBlock(models.Model):
    """Block POKEs from specific character"""
    blocker_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_poke_senders'
    )
    blocked_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_poke_receivers'
    )
    blocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(
        max_length=200,
        blank=True,
        help_text='Optional reason for blocking'
    )
    
    class Meta:
        unique_together = ('blocker_character', 'blocked_character')
        indexes = [
            models.Index(fields=['blocker_character', 'blocked_character']),
        ]
    
    def __str__(self):
        return f"{self.blocker_character.nickname} blocked {self.blocked_character.nickname}"


class CharacterBlock(models.Model):
    """
    General blocking between characters.
    Blocks messages, friend requests, and all interactions.
    """
    blocker_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_characters'  # Characters I blocked
    )
    blocked_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='blocked_by_characters'  # Characters that blocked me
    )
    blocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(
        max_length=500,
        blank=True,
        help_text='Optional reason for blocking (not shown to blocked user)'
    )
    # Optional: report as spam/harassment
    reported_as_spam = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('blocker_character', 'blocked_character')
        indexes = [
            models.Index(fields=['blocker_character', 'blocked_at']),
            models.Index(fields=['blocked_character']),
        ]
        ordering = ['-blocked_at']
    
    def __str__(self):
        return f"{self.blocker_character.nickname} blocked {self.blocked_character.nickname}"
