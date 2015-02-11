import factory

from bughouse.models import (
    Player,
    Team,
    Game,
    PlayerRating,
    TeamRating,
    OVERALL_OVERALL,
)


class PlayerFactory(factory.DjangoModelFactory):
    name = factory.Sequence("player-{0}".format)
    icon = factory.django.ImageField(from_path="tests/yoav.jpg")

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


class PlayerRatingFactory(factory.DjangoModelFactory):
    player = factory.SubFactory(PlayerFactory)
    game = factory.SubFactory(
        GameFactory,
        winning_team=factory.SubFactory(
            TeamFactory,
            white_player=factory.SelfAttribute('...player'),
        ),
    )
    key = OVERALL_OVERALL

    @factory.post_generation
    def rating(self, create, extracted, **kwargs):
        if extracted is not None:
            self.rating = extracted
            self.save()

    class Meta:
        model = PlayerRating
        django_get_or_create = ('game', 'player')


class TeamRatingFactory(factory.DjangoModelFactory):
    team = factory.SubFactory(TeamFactory)
    game = factory.SubFactory(GameFactory, winning_team=factory.SelfAttribute('..team'))
    key = OVERALL_OVERALL

    @factory.post_generation
    def rating(self, create, extracted, **kwargs):
        if extracted is not None:
            self.rating = extracted
            self.save()

    class Meta:
        model = TeamRating
        django_get_or_create = ('game', 'team')
