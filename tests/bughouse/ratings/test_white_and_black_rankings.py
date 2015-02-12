from bughouse.models import (
    BLACK,
    WHITE,
    OVERALL_OVERALL,
    OVERALL_WHITE,
    OVERALL_BLACK,
)


def test_black_white_player_ratings(factories, models, elo_settings):
    player = factories.PlayerFactory()
    team_a = factories.TeamFactory(white_player=player)
    team_b = factories.TeamFactory(black_player=player)

    factories.GameFactory(winning_team=team_a, losing_color=BLACK)

    assert player.get_latest_rating(key=OVERALL_OVERALL) == 1028
    assert player.get_latest_rating(key=OVERALL_WHITE) == 1028
    assert player.get_latest_rating(key=OVERALL_BLACK) == 1000

    factories.GameFactory(winning_team=team_b, losing_color=WHITE)

    assert player.get_latest_rating(key=OVERALL_OVERALL) == 1056
    assert player.get_latest_rating(key=OVERALL_WHITE) == 1028
    assert player.get_latest_rating(key=OVERALL_BLACK) == 1028

    factories.GameFactory(winning_team=team_a, losing_color=BLACK)

    assert player.get_latest_rating(key=OVERALL_OVERALL) == 1080
    assert player.get_latest_rating(key=OVERALL_WHITE) == 1056
    assert player.get_latest_rating(key=OVERALL_BLACK) == 1028
