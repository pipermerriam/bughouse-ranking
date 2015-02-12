from bughouse.ratings.engines import compute_ratings_for_game


def compute_ratings(sender, instance, created, raw, **kwargs):
    if not raw:
        compute_ratings_for_game(instance)
