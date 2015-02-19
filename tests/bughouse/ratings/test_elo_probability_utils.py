import pytest

from bughouse.ratings.utils import (
    elo_chance_to_lose,
    elo_chance_to_win,
)


def assert_almost_equal(v1, v2, delta=0.01):
    assert abs(v1 - v2) < delta


@pytest.mark.parametrize(
    "score_a,score_b,chance",
    (
        (1000, 1000, 0.5),
        (500, 500, 0.5),
        (1500, 1500, 0.5),
        (1100, 900, 0.75),
        (900, 700, 0.75),
        (1100, 1000, 0.64),
        (1000, 900, 0.64),
    ),
)
def test_even_chance(score_a, score_b, chance):
    assert_almost_equal(elo_chance_to_win(score_a, score_b), chance)
    assert_almost_equal(elo_chance_to_lose(score_a, score_b), 1 - chance)
