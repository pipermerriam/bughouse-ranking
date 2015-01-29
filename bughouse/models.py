from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Team(models.Model):
    white_player = models.ForeignKey('Player', related_name='teams_as_white')
    black_player = models.ForeignKey('Player', related_name='teams_as_black')

    class Meta:
        unique_together = (
            ('white_player', 'black_player'),
        )


WHITE = 'white'
BLACK = 'black'

UNKNOWN = 'unknown'
CHECKMATE = 'checkmate'
TIME = 'time'
SWINDLE = 'swindle'
IMMINENT_DEATH = 'imminent-death'


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class AbstractRating(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rating = models.FloatField()


class TeamRating(AbstractRating):
    game = models.ForeignKey('Game', related_name="team_ratings")
    team = models.ForeignKey('Team', related_name="ratings")


class PlayerRating(AbstractRating):
    game = models.ForeignKey('Game', related_name="player_ratings")
    player = models.ForeignKey('Player', related_name="ratings")
