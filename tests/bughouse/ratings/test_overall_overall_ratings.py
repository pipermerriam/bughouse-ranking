import pytest

from bughouse.models import (
    BLACK,
    WHITE,
    OVERALL_OVERALL,
)
from bughouse.ratings.engines.overall import (
    rate_teams,
    rate_players,
    provisional_modifier,
)


def test_rate_single_game(factories, models, elo_settings):
    game = factories.GameFactory()
    r1, r2 = rate_teams(game)

    assert r1.rating == 1024
    assert r2.rating == 976


def test_rate_multiple_games(factories, models):
    team_a = factories.TeamFactory()
    team_b = factories.TeamFactory()
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))

    assert team_a.get_latest_rating(OVERALL_OVERALL) == 1052
    assert team_b.get_latest_rating(OVERALL_OVERALL) == 948


def test_provisional_limit(factories, models):
    team_a = factories.TeamFactory()
    team_b = factories.TeamFactory()

    assert provisional_modifier(team_a) == 4

    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))

    assert provisional_modifier(team_a) == 4

    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))
    rate_teams(factories.GameFactory(winning_team=team_a, losing_team=team_b))

    assert team_a.total_games == 11
    assert provisional_modifier(team_a) == 1
    assert (
        team_a.get_latest_rating(OVERALL_OVERALL) > team_b.get_latest_rating(OVERALL_OVERALL)
    )
    assert (
        team_a.get_latest_rating(OVERALL_OVERALL) + team_b.get_latest_rating(OVERALL_OVERALL)
    ) / 2 == 1000


@pytest.mark.parametrize(
    'losing_color',
    (BLACK, WHITE),
)
def test_individual_ratings(factories, models, losing_color):
    game = factories.GameFactory(losing_color=losing_color)

    if game.losing_color == game.BLACK:
        wtwr, wtbr, ltwr, ltbr = rate_players(game)

        assert wtwr.player.get_latest_rating(OVERALL_OVERALL) == 1028
        assert wtbr.player.get_latest_rating(OVERALL_OVERALL) == 1024
        assert ltwr.player.get_latest_rating(OVERALL_OVERALL) == 976
        assert ltbr.player.get_latest_rating(OVERALL_OVERALL) == 972

    else:
        wtwr, wtbr, ltwr, ltbr = rate_players(game)

        assert wtwr.player.get_latest_rating(OVERALL_OVERALL) == 1024
        assert wtbr.player.get_latest_rating(OVERALL_OVERALL) == 1028
        assert ltwr.player.get_latest_rating(OVERALL_OVERALL) == 972
        assert ltbr.player.get_latest_rating(OVERALL_OVERALL) == 976


def test_ratings_computation_is_idempotent(factories, models):
    """
    Ensure that going back and re-computing old game ratings is an idempotent
    process.
    """
    team_a = factories.TeamFactory()
    team_b = factories.TeamFactory()

    factories.GameFactory(winning_team=team_a, losing_team=team_b)
    game_b = factories.GameFactory(winning_team=team_a, losing_team=team_b)
    factories.GameFactory(winning_team=team_a, losing_team=team_b)

    first_rating_initial = team_a.ratings.get(
        game=game_b,
    ).rating

    rate_teams(game_b)

    first_rating_recomputed = team_a.ratings.get(
        game=game_b,
    ).rating

    assert first_rating_initial == first_rating_recomputed
