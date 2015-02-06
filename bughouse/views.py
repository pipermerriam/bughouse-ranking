from django.utils import timezone
from django.views import generic

from bughouse.models import (
    Player,
    get_icon_url,
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


class CreatePlayerView(generic.CreateView):
    model = Player
    template_name = 'bughouse/create-player.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreatePlayerView, self).get_context_data(**kwargs)
        context['available_icons'] = self.get_available_icons()
        return context

    def get_available_icons(self):
        used_icons = set(Player.objects.exclude(
            icon=Player.DEFAULT_ICON,
        ).values_list('icon', flat=True))
        available_icons = tuple((
            value for value in Player.ICON_CHOICES if value[0] not in used_icons
        ))
        return tuple((
            (v[0], get_icon_url(v[0]), v[1]) for v in available_icons
        ))


class TeamLeaderboard(generic.ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'bughouse/team-leaderboard.html'

    def get_queryset(self):
        qs = super(TeamLeaderboard, self).get_queryset()
        return sorted(qs, key=lambda team: team.latest_rating, reverse=True)


class IndividualLeaderboard(generic.ListView):
    model = Player
    context_object_name = 'players'
    template_name = 'bughouse/individual-leaderboard.html'

    def get_queryset(self):
        qs = super(IndividualLeaderboard, self).get_queryset()
        return sorted(qs, key=lambda player: player.latest_rating, reverse=True)


class PlayerRatingsVisualization(PlayerDataMixin, generic.TemplateView):
    template_name = 'bughouse/player-rating-visualization.html'
