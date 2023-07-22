from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons/')

    def __str__(self):
        return self.name

class Account(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    facebook = models.URLField(blank=True)
    twitch = models.URLField(blank=True)
    gender = models.CharField(
        max_length=6, 
        choices=[('MALE', 'MALE'),('FEMALE', 'FEMALE')]
    )

    def __str__(self):
        return self.user.username

class Character(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    nickname = models.TextField()
    description = models.TextField()
    visibility = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.nickname}"

class GamePlayed(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date_range_start = models.DateField()
    date_range_end = models.DateField()

    def __str__(self):
        return f"{self.character} - {self.game} - {self.date_range_start} to {self.date_range_end}"

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

