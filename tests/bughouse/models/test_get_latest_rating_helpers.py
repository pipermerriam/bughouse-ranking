from bughouse.models import (
    OVERALL_OVERALL,
)


def test_player_get_latest_rating(factories):
    player = factories.PlayerFactory()

    factories.PlayerRatingFactory(player=player, force_rating=900)
    factories.PlayerRatingFactory(player=player, force_rating=1100)

    assert player.get_latest_rating(OVERALL_OVERALL) == 1100


def test_team_get_latest_rating(factories):
    team = factories.TeamFactory()

    factories.TeamRatingFactory(team=team, force_rating=900)
    factories.TeamRatingFactory(team=team, force_rating=1100)

    assert team.get_latest_rating(OVERALL_OVERALL) == 1100


def test_player_get_rating_at_datetime(factories):
    player = factories.PlayerFactory()

    first = factories.PlayerRatingFactory(player=player, force_rating=900)
    middle = factories.PlayerRatingFactory(player=player, force_rating=2000)
    last = factories.PlayerRatingFactory(player=player, force_rating=1100)

    # sanity check
    assert first.created_at < middle.created_at < last.created_at

    assert player.get_rating_at_datetime(middle.created_at, key=middle.key) == 2000


def test_team_get_rating_at_datetime(factories):
    team = factories.TeamFactory()

    first = factories.TeamRatingFactory(team=team, force_rating=900)
    middle = factories.TeamRatingFactory(team=team, force_rating=2000)
    last = factories.TeamRatingFactory(team=team, force_rating=1100)

    # sanity check
    assert first.created_at < middle.created_at < last.created_at

    assert team.get_rating_at_datetime(middle.created_at, key=middle.key) == 2000


def test_player_get_rating_at_datetime_with_specified_key(factories):
    player = factories.PlayerFactory()

    key_a = 'test:a'
    key_b = 'test:b'

    first_a = factories.PlayerRatingFactory(player=player, rating=800, key=key_a)
    first_b = factories.PlayerRatingFactory(player=player, rating=900, key=key_b)
    middle_a = factories.PlayerRatingFactory(player=player, rating=1000, key=key_a)
    middle_b = factories.PlayerRatingFactory(player=player, rating=1100, key=key_b)
    last_a = factories.PlayerRatingFactory(player=player, rating=1200, key=key_a)
    last_b = factories.PlayerRatingFactory(player=player, rating=1300, key=key_b)

    # sanity check
    assert first_a.created_at < first_b.created_at < middle_a.created_at < middle_b.created_at < last_a.created_at < last_b.created_at

    assert player.get_rating_at_datetime(middle_a.created_at, key=middle_a.key) == 1000
    assert player.get_rating_at_datetime(middle_b.created_at, key=middle_b.key) == 1100
