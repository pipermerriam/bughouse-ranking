class BaseRatingsEngine(object):
    def compute_ratings(self, game):
        raise NotImplemented("Subclasses must implement a `compute_ratings` method")
