def test_player_get_latest_rating(factories):
    player = factories.PlayerFactory()

    factories.PlayerRatingFactory(player=player, rating=900)
    factories.PlayerRatingFactory(player=player, rating=1100)

    assert player.latest_rating == 1100


def test_team_get_latest_rating(factories):
    team = factories.TeamFactory()

    factories.TeamRatingFactory(team=team, rating=900)
    factories.TeamRatingFactory(team=team, rating=1100)

    assert team.latest_rating == 1100


def test_player_get_rating_at_datetime(factories):
    player = factories.PlayerFactory()

    first = factories.PlayerRatingFactory(player=player, rating=900)
    middle = factories.PlayerRatingFactory(player=player, rating=2000)
    last = factories.PlayerRatingFactory(player=player, rating=1100)

    # sanity check
    assert first.created_at < middle.created_at < last.created_at

    assert player.get_rating_at_datetime(middle.created_at) == 2000


def test_team_get_rating_at_datetime(factories):
    team = factories.TeamFactory()

    first = factories.TeamRatingFactory(team=team, rating=900)
    middle = factories.TeamRatingFactory(team=team, rating=2000)
    last = factories.TeamRatingFactory(team=team, rating=1100)

    # sanity check
    assert first.created_at < middle.created_at < last.created_at

    assert team.get_rating_at_datetime(middle.created_at) == 2000
