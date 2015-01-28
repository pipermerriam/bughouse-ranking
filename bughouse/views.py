from django.utils import timezone
from django.views import generic

from bughouse.models import (
    Player,
    Game,
)
from bughouse.api.v1.serializers import (
    GameSerializer,
)


class ReportGameView(generic.TemplateView):
    template_name = 'bughouse/report-game.html'

    def get_context_data(self, **kwargs):
        context = super(ReportGameView, self).get_context_data(**kwargs)
        context['players'] = Player.objects.values('id', "name")
        context['recent_games'] = self.get_recent_games_data()
        return context

    def get_recent_games_data(self):
        day_ago = timezone.now() - timezone.timedelta(1)
        qs = Game.objects.filter(created_at__gte=day_ago).order_by('-created_at')[:5]
        serializer = GameSerializer(qs, many=True)
        return serializer.data
