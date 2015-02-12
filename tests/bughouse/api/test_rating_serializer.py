from bughouse.api.v1.serializers import PlayerRatingSerializer


def test_rating_serialization(factories):
    rating = factories.PlayerRatingFactory()
    serializer = PlayerRatingSerializer(rating)
    data = serializer.data

    # smoke test
    assert data['id'] == rating.pk
