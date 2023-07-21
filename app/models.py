# game_player_nick_finder/app/models.py
from django.db import models

class YourModel(models.Model):
    # Dodaj swoje pola modelu
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
    
    def __str__(self):
        return self.field1
