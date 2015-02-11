import base64

from django.core.files.base import ContentFile

from sorl.thumbnail import get_thumbnail

from rest_framework import serializers

from bughouse.models import (
    Player,
    Team,
    Game,
    PlayerRating,
)


class PlayerIconField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['read_only'] = True
        self.dimensions = kwargs.pop("dimensions")
        super(PlayerIconField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        im = get_thumbnail(value, self.dimensions, crop='center', quality=99, format="PNG")
        return im.url


class B64ImageField(serializers.CharField):
    def to_internal_value(self, value):
        return ContentFile(base64.b64decode(value))

    def to_representation(self, value):
        with value.open('r') as image_file:
            return base64.b64encode(image_file.read())


class PlayerSerializer(serializers.ModelSerializer):
    icon_url = PlayerIconField(dimensions="200x200", source="icon")
    icon = B64ImageField(write_only=True, required=False)
    icon_filename = serializers.CharField(write_only=True, required=False)

    latest_rating = serializers.FloatField(read_only=True)
    total_games = serializers.IntegerField(read_only=True)

    def validate(self, data):
        icon = data.get('icon')
        icon_filename = data.get('icon_filename')
        if bool(icon) is not bool(icon_filename):
            raise serializers.ValidationError(
                "`icon` and `icon_filename` are required to update the icon",
            )
        return super(PlayerSerializer, self).validate(data)

    def validate_icon(self, value):
        if not value and self.instance is None:
            raise serializers.ValidationError(
                "`icon` is required for player creation"
            )
        return value

    def validate_icon_filename(self, value):
        if not value and self.instance is None:
            raise serializers.ValidationError(
                "`icon_filename` is required for player creation"
            )
        return value

    class Meta:
        model = Player
        fields = (
            'id',
            'name',
            'icon',
            'icon_filename',
            'icon_url',
            'is_active',
            'total_games',
            'latest_rating',
        )

    def save(self, *args, **kwargs):
        icon_filename = self.validated_data.pop("icon_filename", None)
        icon = self.validated_data.pop('icon', None)
        player = super(PlayerSerializer, self).save(*args, **kwargs)
        if icon_filename and icon:
            player.icon.save(
                icon_filename,
                icon,
                save=True,
            )
        return player


class PlayerField(serializers.IntegerField):
    def to_internal_value(self, value):
        try:
            return Player.objects.get(id=value)
        except Player.DoesNotExist:
            raise serializers.ValidationError("Unknown player")

    def to_representation(self, value):
        return value.pk


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


class PlayerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRating
        fields = (
            'id',
            'created_at',
            'updated_at',
            'player',
            'key',
            'game',
            'rating',
        )
        read_only_fields = fields
