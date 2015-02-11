def win_probability_from_rating(r1, r2):
    diff = r1 - r2
    return 1.0 / (pow(10, (diff / 400.0)) + 1.0)
