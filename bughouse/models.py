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


class Rated(Timestamped):
    class Meta(Timestamped.Meta):
        abstract = True

    def get_latest_rating(self, key):
        rating = self.ratings.filter(key=key).first()
        if rating:
            return rating.rating
        else:
            return INITIAL_RATING

    def get_rating_at_datetime(self, when, key):
        rating = self.ratings.filter(created_at__lt=when, key=key).first()
        if rating:
            return rating.rating
        else:
            return INITIAL_RATING


INITIAL_RATING = 1000


@python_2_unicode_compatible
class Player(Rated):
    name = models.CharField(max_length=255, unique=True)
    icon = models.ImageField()

    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def total_games(self):
        return Game.objects.filter(
            Q(winning_team__white_player=self) |
            Q(winning_team__black_player=self) |
            Q(losing_team__white_player=self) |
            Q(losing_team__black_player=self)
        ).distinct().count()


class Team(Rated):
    white_player = models.ForeignKey('Player', related_name='teams_as_white',
                                     on_delete=models.PROTECT)
    black_player = models.ForeignKey('Player', related_name='teams_as_black',
                                     on_delete=models.PROTECT)

    class Meta(Rated.Meta):
        unique_together = (
            ('white_player', 'black_player'),
        )

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


EXPERIMENTAL_BATMAN = 'experimental:batman'
OVERALL_OVERALL = 'overall:overall'
OVERALL_WHITE = 'overall:white'
OVERALL_BLACK = 'overall:black'


class TeamRating(Timestamped):
    rating = models.FloatField()

    key = models.CharField(max_length=255)
    game = models.ForeignKey('Game', related_name="team_ratings")
    team = models.ForeignKey('Team', related_name="ratings")

    class Meta(Timestamped.Meta):
        unique_together = (
            ('game', 'team', 'key'),
        )

    def save(self, *args, **kwargs):
        if self.game:
            self.created_at = self.game.created_at
        super(TeamRating, self).save(*args, **kwargs)


@python_2_unicode_compatible
class PlayerRating(Timestamped):
    rating = models.FloatField()

    key = models.CharField(max_length=255)
    game = models.ForeignKey('Game', related_name="player_ratings")
    player = models.ForeignKey('Player', related_name="ratings")

    class Meta(Timestamped.Meta):
        unique_together = (
            ('game', 'player', 'key'),
        )

    def save(self, *args, **kwargs):
        if self.game:
            self.created_at = self.game.created_at
        super(PlayerRating, self).save(*args, **kwargs)

    def __str__(self):
        return "{s.player} - {s.key} - {s.rating}".format(s=self)
