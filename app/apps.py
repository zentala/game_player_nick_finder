# game_player_nick_finder/app/apps.py
from django.apps import AppConfig

class AppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals

default_app_config = 'app.apps.AppNameConfig'
