from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import viewsets
from rest_framework import exceptions

from bughouse.models import (
    Game,
    Player,
    PlayerRating,
)

from .serializers import (
    GameSerializer,
    PlayerSerializer,
    PlayerRatingSerializer,
)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def delete(self):
        instance = self.get_object()
        ten_minutes_ago = timezone.now() - timezone.timedelta(seconds=60 * 10)
        if instance.created_at < ten_minutes_ago:
            raise exceptions.PermissionDenied("Cannot delete games older than 10 minutes")
        return super(GameViewSet, self).delete()


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerRatingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlayerRating.objects.all()
    serializer_class = PlayerRatingSerializer

    def get_queryset(self):
        player = get_object_or_404(Player, pk=self.kwargs['player_pk'])
        return player.ratings.all()
