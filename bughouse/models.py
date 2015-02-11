from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


class Timestamped(models.Model):
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


INITIAL_RATING = 1000


@python_2_unicode_compatible
class Player(Timestamped):
    name = models.CharField(max_length=255, unique=True)
    icon = models.ImageField()

    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def latest_rating(self):
        rating = self.ratings.first()
        if rating:
            return rating.rating
        else:
            return INITIAL_RATING

    @property
    def total_games(self):
        return Game.objects.filter(
            Q(winning_team__white_player=self) |
            Q(winning_team__black_player=self) |
            Q(losing_team__white_player=self) |
            Q(losing_team__black_player=self)
        ).distinct().count()


class Team(Timestamped):
    white_player = models.ForeignKey('Player', related_name='teams_as_white',
                                     on_delete=models.PROTECT)
    black_player = models.ForeignKey('Player', related_name='teams_as_black',
                                     on_delete=models.PROTECT)

    class Meta(Timestamped.Meta):
        unique_together = (
            ('white_player', 'black_player'),
        )

    @property
    def latest_rating(self):
        rating = self.ratings.first()
        if rating:
            return rating.rating
        else:
            return INITIAL_RATING

    @property
    def total_games(self):
        return Game.objects.filter(
            Q(winning_team=self) |
            Q(losing_team=self)
        ).distinct().count()


WHITE = 'white'
BLACK = 'black'

UNKNOWN = 'unknown'
CHECKMATE = 'checkmate'
TIME = 'time'
SWINDLE = 'swindle'
IMMINENT_DEATH = 'imminent-death'


class Game(Timestamped):
    winning_team = models.ForeignKey('Team', related_name='game_wins')
    losing_team = models.ForeignKey('Team', related_name='game_losses')
    WHITE = WHITE
    BLACK = BLACK
    COLOR_CHOICES = (
        (WHITE, 'White'),
        (BLACK, 'Black'),
    )
    losing_color = models.CharField(max_length=20, choices=COLOR_CHOICES)

    UNKNOWN = UNKNOWN
    CHECKMATE = CHECKMATE
    TIME = TIME
    SWINDLE = SWINDLE
    IMMINENT_DEATH = IMMINENT_DEATH
    LOSS_TYPE_CHOICES = (
        (CHECKMATE, 'Checkmate'),
        (TIME, 'Time'),
        (SWINDLE, 'Swindle'),
        (IMMINENT_DEATH, 'Imminent Death'),
    )
    loss_type = models.CharField(max_length=20, choices=LOSS_TYPE_CHOICES,
                                 blank=True, default=UNKNOWN)


class TeamRating(Timestamped):
    rating = models.FloatField()

    game = models.ForeignKey('Game', related_name="team_ratings")
    team = models.ForeignKey('Team', related_name="ratings")


class PlayerRating(Timestamped):
    rating = models.FloatField()

    game = models.ForeignKey('Game', related_name="player_ratings")
    player = models.ForeignKey('Player', related_name="ratings")
