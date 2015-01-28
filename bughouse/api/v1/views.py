from django.utils import timezone

from rest_framework import viewsets
from rest_framework import exceptions

from bughouse.models import Game

from .serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def delete(self):
        instance = self.get_object()
        ten_minutes_ago = timezone.now() - timezone.timedelta(seconds=60 * 10)
        if instance.created_at < ten_minutes_ago:
            raise exceptions.PermissionDenied("Cannot delete games older than 10 minutes")
        return super(GameViewSet, self).delete()
