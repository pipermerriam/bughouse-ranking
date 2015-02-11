# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_team_rating_keys(apps, schema_editor):
    TeamRating = apps.get_model("bughouse", "TeamRating")
    TeamRating.objects.update(key='overall:overall')


def populate_player_rating_keys(apps, schema_editor):
    PlayerRating = apps.get_model("bughouse", "PlayerRating")
    PlayerRating.objects.update(key='overall:overall')


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0006_auto_20150211_2025'),
    ]

    operations = [
        migrations.RunPython(populate_team_rating_keys),
        migrations.RunPython(populate_player_rating_keys),
    ]
