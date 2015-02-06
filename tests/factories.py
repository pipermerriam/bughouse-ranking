import factory

from bughouse.models import (
    Player,
    Team,
    Game,
)



class PlayerFactory(factory.DjangoModelFactory):
    name = factory.Sequence("player-{0}".format)

    class Meta:
        model = Player
        django_get_or_create = ('name',)


class TeamFactory(factory.DjangoModelFactory):
    white_player = factory.SubFactory(PlayerFactory)
    black_player = factory.SubFactory(PlayerFactory)

    class Meta:
        model = Team
        django_get_or_create = ('white_player', 'black_player')


class GameFactory(factory.DjangoModelFactory):
    winning_team = factory.SubFactory(TeamFactory)
    losing_team = factory.SubFactory(TeamFactory)
    losing_color = 'black'
    loss_type = 'checkmate'

    class Meta:
        model = Game
