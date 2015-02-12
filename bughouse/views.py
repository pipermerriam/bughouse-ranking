from django.utils import timezone
from django.views import generic

from bughouse.models import (
    OVERALL_OVERALL,
    Player,
    Game,
    Team,
)
from bughouse.api.v1.serializers import (
    PlayerSerializer,
    GameSerializer,
)


class PlayerDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PlayerDataMixin, self).get_context_data(**kwargs)
        context['players'] = self.get_player_data()
        return context

    def get_player_data(self):
        qs = Player.objects.all()
        serializer = PlayerSerializer(qs, many=True)
        return serializer.data


class ReportGameView(PlayerDataMixin, generic.TemplateView):
    template_name = 'bughouse/report-game.html'

    def get_context_data(self, **kwargs):
        context = super(ReportGameView, self).get_context_data(**kwargs)
        context['recent_games'] = self.get_recent_games_data()
        return context

    def get_recent_games_data(self):
        day_ago = timezone.now() - timezone.timedelta(1)
        qs = Game.objects.filter(created_at__gte=day_ago).order_by('-created_at')[:5]
        serializer = GameSerializer(qs, many=True)
        return serializer.data


class TeamLeaderboard(generic.ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'bughouse/team-leaderboard.html'

    def get_queryset(self):
        qs = super(TeamLeaderboard, self).get_queryset()
        return sorted(qs, key=lambda team: team.get_latest_rating(OVERALL_OVERALL), reverse=True)


class IndividualLeaderboard(generic.ListView):
    model = Player
    context_object_name = 'players'
    template_name = 'bughouse/individual-leaderboard.html'

    def get_queryset(self):
        qs = super(IndividualLeaderboard, self).get_queryset()
        return sorted(qs, key=lambda player: player.get_latest_rating(OVERALL_OVERALL), reverse=True)


class PlayerRatingsVisualization(PlayerDataMixin, generic.TemplateView):
    template_name = 'bughouse/player-rating-visualization.html'


class PlayerRosterView(PlayerDataMixin, generic.TemplateView):
    template_name = 'bughouse/player-roster.html'
