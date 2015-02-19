class BaseRatingsEngine(object):
    def compute_ratings(self, game):
        raise NotImplemented("Subclasses must implement a `compute_ratings` method")

    def adjust_rating(self, player, player_partner, opponent, opponent_partner):
        raise NotImplemented("Subclasses must implement a `adjust_ratings` method")
