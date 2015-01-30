from rest_framework import serializers

from bughouse.models import (
    Player,
    Team,
    Game,
)


class PlayerField(serializers.IntegerField):
    def to_internal_value(self, value):
        try:
            return Player.objects.get(id=value)
        except Player.DoesNotExist:
            raise serializers.ValidationError("Unknown player")

    def to_representation(self, value):
        return value.pk


class PlayerSerializer(serializers.ModelSerializer):
    icon_url = serializers.CharField()

    class Meta:
        model = Player
        fields = (
            'id',
            'name',
            'icon_url',
        )


class GameSerializer(serializers.ModelSerializer):
    winning_team_white = PlayerField(source="winning_team.white_player")
    winning_team_black = PlayerField(source="winning_team.black_player")
    losing_team_white = PlayerField(source="losing_team.white_player")
    losing_team_black = PlayerField(source="losing_team.black_player")

    def to_internal_value(self, data):
        ret = super(GameSerializer, self).to_internal_value(data)
        wtw = ret['winning_team']['white_player']
        wtb = ret['winning_team']['black_player']
        ltw = ret['losing_team']['white_player']
        ltb = ret['losing_team']['black_player']

        if len(set((wtw.pk, wtb.pk, ltw.pk, ltb.pk))) != 4:
            raise serializers.ValidationError("Players must be unique")

        ret['winning_team'], _ = Team.objects.get_or_create(
            white_player=wtw,
            black_player=wtb,
        )
        ret['losing_team'], _ = Team.objects.get_or_create(
            white_player=ltw,
            black_player=ltb,
        )
        return ret

    class Meta:
        model = Game
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )
        fields = (
            'id',
            'created_at',
            'updated_at',
            'winning_team_white',
            'winning_team_black',
            'losing_team_white',
            'losing_team_black',
            'losing_color',
            'loss_type',
        )
