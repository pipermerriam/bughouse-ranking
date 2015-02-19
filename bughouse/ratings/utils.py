import decimal


def elo_chance_to_lose(player, opponent):
    """
    Probability = 1 / (1 + (10 ^ -((White Rating - Black Rating) / 400)))
    """
    diff = player - opponent
    return 1.0 / (1 + pow(10, (diff / 400.0)))


def elo_chance_to_win(player, opponent):
    return 1 - elo_chance_to_lose(player, opponent)


def round_it(num):
    """
    An integer rounding function that uses `ROUND_HALF_EVEN`.
    """
    return int(
        decimal.Decimal(num).quantize(
            decimal.Decimal('1'),
            rounding=decimal.ROUND_HALF_EVEN,
        )
    )
