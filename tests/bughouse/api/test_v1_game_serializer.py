from bughouse.api.v1.serializers import GameSerializer


def test_lazy_team_creation(factories, models):
    wtw = factories.PlayerFactory()
    wtb = factories.PlayerFactory()
    ltw = factories.PlayerFactory()
    ltb = factories.PlayerFactory()

    data = {
        'winning_team_white': wtw.pk,
        'winning_team_black': wtb.pk,
        'losing_team_white': ltw.pk,
        'losing_team_black': ltb.pk,
        'losing_color': 'white',
        'loss_type': 'checkmate',
    }

    # sanity check
    assert not models.Team.objects.exists()

    serializer = GameSerializer(data=data)
    assert serializer.is_valid()
    game = serializer.save()

    assert game.winning_team.white_player == wtw
    assert game.winning_team.black_player == wtb
    assert game.losing_team.white_player == ltw
    assert game.losing_team.black_player == ltb

    assert models.Team.objects.count() == 2


def test_existing_teams(factories, models):
    winning_team = factories.TeamFactory()
    losing_team = factories.TeamFactory()
    wtw = winning_team.white_player
    wtb = winning_team.black_player
    ltw = losing_team.white_player
    ltb = losing_team.black_player

    data = {
        'winning_team_white': wtw.pk,
        'winning_team_black': wtb.pk,
        'losing_team_white': ltw.pk,
        'losing_team_black': ltb.pk,
        'losing_color': 'white',
        'loss_type': 'checkmate',
    }

    # sanity check
    assert models.Team.objects.count() == 2

    serializer = GameSerializer(data=data)
    assert serializer.is_valid()
    game = serializer.save()

    assert game.winning_team.white_player == wtw
    assert game.winning_team.black_player == wtb
    assert game.losing_team.white_player == ltw
    assert game.losing_team.black_player == ltb

    assert models.Team.objects.count() == 2


def test_game_serialization(factories):
    game = factories.GameFactory()
    serializer = GameSerializer(game)
    data = serializer.data
    assert data['winning_team_white'] == game.winning_team.white_player.pk
    assert data['winning_team_black'] == game.winning_team.black_player.pk
    assert data['losing_team_white'] == game.losing_team.white_player.pk
    assert data['losing_team_black'] == game.losing_team.black_player.pk
