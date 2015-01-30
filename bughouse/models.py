import os

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.staticfiles.storage import staticfiles_storage


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


INITIAL_RATING = 1000


DEFAULT_ICON = ('default.jpg', 'Default')
ICON_CHOICES = (
    DEFAULT_ICON,
    ('blake.jpg', 'Blake'),
    ('johnny.jpg', 'Johnny'),
    ('josh.jpg', 'Josh'),
    ('kit.jpg', 'Kit'),
    ('marla.jpg', 'Marla'),
    ('piper.jpg', 'Piper'),
    ('than.jpg', 'Than'),
    ('brian.jpg', 'Brian'),
    ('jon.jpg', 'Jon'),
    ('kevin.jpg', 'Kevin'),
    ('kyle.jpg', 'Kyle'),
    ('nathan.jpg', 'Nathan'),
    ('remi.jpg', 'Remi'),
    ('yoav.jpg', 'Yoav'),
)


class Player(Timestamped):
    name = models.CharField(max_length=255, unique=True)
    DEFAULT_ICON = DEFAULT_ICON
    ICON_CHOICES = ICON_CHOICES
    icon = models.CharField(max_length=20, blank=True, default=DEFAULT_ICON[0])

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

    @property
    def icon_url(self):
        icon = self.icon or self.DEFAULT_ICON[0]
        path = os.path.join('images', 'player-icons', icon)
        return staticfiles_storage.url(path)

    def clean_fields(self, *args, **kwargs):
        super(Player, self).clean_fields(*args, **kwargs)
        if self.icon != self.DEFAULT_ICON:
            if Player.objects.exclude(id=self.pk).filter(icon=self.icon).exists():
                raise ValidationError("Icon is taken")


class Team(Timestamped):
    white_player = models.ForeignKey('Player', related_name='teams_as_white')
    black_player = models.ForeignKey('Player', related_name='teams_as_black')

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
            Q(winning_team__white_player=self) |
            Q(winning_team__black_player=self) |
            Q(losing_team__white_player=self) |
            Q(losing_team__black_player=self)
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
