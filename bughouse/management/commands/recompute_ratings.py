from django.core.management.base import BaseCommand

from bughouse.models import Game
from bughouse.ratings.engines import compute_ratings_for_game


class Command(BaseCommand):
    help = 'Recompute all ratings using all active engines'

    def handle(self, *args, **options):
        for game in Game.objects.order_by('created_at').all():
            compute_ratings_for_game(game)
