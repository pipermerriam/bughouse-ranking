from django.conf import settings
from django.core.files.storage import default_storage

from bughouse.api.v1.serializers import PlayerSerializer


def test_icon_url_serialization(factories):
    player = factories.PlayerFactory()
    data = PlayerSerializer(player).data

    assert data['icon_url'].startswith(settings.MEDIA_URL)
    assert default_storage.exists(data['icon_url'][len(settings.MEDIA_URL):])
