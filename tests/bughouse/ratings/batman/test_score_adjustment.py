import pytest

from bughouse.ratings.engines.batman import adjust_ratings


@pytest.mark.parametrize(
    "base_ratings,expected",
    (
        # Matchup A
        ((1050, 950, 900, 1100), 894),  # 23 %
        ((950, 1050, 1100, 900), 1106),  # 77 %
        # Matchup B
        ((1000, 1000, 950, 1050), 958),  # 38 %
        ((1000, 1000, 1050, 950), 1042),  # 62 %
    ),
)
def test_adjusted_scores(base_ratings, expected):
    actual = adjust_ratings(*base_ratings, scalar=3)

    assert actual == expected
