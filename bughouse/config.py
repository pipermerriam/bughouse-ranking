from django.apps import AppConfig
from django import dispatch
from django.db.models.signals import post_save

class BughouseConfig(AppConfig):
    name = 'bughouse'

    def ready(self):
        from bughouse.receivers import compute_game_ratings
        dispatch.receiver(post_save, sender='bughouse.Game')(
                            compute_game_ratings,
                            )
