import base64

import pytest

from django.conf import settings
from django.core.files.storage import default_storage

from bughouse.api.v1.serializers import PlayerSerializer


def test_icon_url_serialization(factories):
    player = factories.PlayerFactory()
    data = PlayerSerializer(player).data

    assert data['icon_url'].startswith(settings.MEDIA_URL)
    assert default_storage.exists(data['icon_url'][len(settings.MEDIA_URL):])


@pytest.mark.django_db
def test_new_player_creation():
    serializer = PlayerSerializer(data={
        'icon_filename': 'yoav.jpg',
        'icon': base64.b64encode(open('tests/yoav.jpg', 'r').read()),
        'name': 'Yoav',
    })
    assert serializer.is_valid(), serializer.errors
    player = serializer.save()
    assert player.name == 'Yoav'
    assert player.icon is not None
    assert player.icon.width == 400
    assert player.icon.height == 400


@pytest.mark.django_db
def test_new_player_icon_name_required_when_icon_present_during_creation():
    serializer = PlayerSerializer(data={
        'icon': base64.b64encode(open('tests/yoav.jpg', 'r').read()),
        'name': 'Yoav',
    })
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_new_player_icon_data_required_when_icon_present_during_creation():
    serializer = PlayerSerializer(data={
        'icon_filename': 'yoav.jpg',
        'name': 'Yoav',
    })
    assert not serializer.is_valid()


def test_new_player_icon_name_required_when_icon_present_during_update(factories):
    player = factories.PlayerFactory()
    serializer = PlayerSerializer(player, data={
        'icon': base64.b64encode(open('tests/yoav.jpg', 'r').read()),
        'name': 'Yoav',
    })
    assert not serializer.is_valid()


def test_new_player_icon_data_required_when_icon_present_during_update(factories):
    player = factories.PlayerFactory()
    serializer = PlayerSerializer(player, data={
        'icon_filename': 'yoav.jpg',
        'name': 'Yoav',
    })
    assert not serializer.is_valid()


def test_player_icon_not_required_for_update(factories):
    player = factories.PlayerFactory(name='Initial')
    serializer = PlayerSerializer(player, data={
        'name': 'Updated',
    })
    assert serializer.is_valid(), serializer.errors
    updated_player = serializer.save()

    assert updated_player.name == 'Updated'
    assert player.icon.name == updated_player.icon.name
