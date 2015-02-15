import decimal


def win_probability_from_rating(r1, r2):
    diff = r1 - r2
    return 1.0 / (pow(10, (diff / 400.0)) + 1.0)


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
