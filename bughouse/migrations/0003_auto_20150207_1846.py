# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db import models, migrations
from django.contrib.staticfiles.finders import find
from django.core.files import File



DEFAULT_ICON = ('default.jpg', 'Default')
ICON_CHOICES = (
    DEFAULT_ICON,
    ('blake.jpg', 'Blake'),
    ('johnny.jpg', 'Johnny'),
    ('josh.jpg', 'Josh'),
    ('kit.jpg', 'Kit'),
    ('marla.jpg', 'Marla'),
    ('piper.jpg', 'Piper'),
    ('than.jpg', 'Than'),
    ('brian.jpg', 'Brian'),
    ('jon.jpg', 'Jon'),
    ('kevin.jpg', 'Kevin'),
    ('kyle.jpg', 'Kyle'),
    ('nathan.jpg', 'Nathan'),
    ('remi.jpg', 'Remi'),
    ('yoav.jpg', 'Yoav'),
)


def populate_player_icons(apps, schema_editor):
    Player = apps.get_model("bughouse", "Player")

    for player in Player.objects.all():
        static_file_name = "{0}.jpg".format(player.name.lower())
        static_image_path = find(os.path.join('images', 'player-icons', static_file_name))
        if static_image_path:
            static_file = open(static_image_path, 'r')
        else:
            static_file = open(find(os.path.join('images', 'player-icons', 'default.jpg')), 'r')
        image_file = File(static_file)
        player.icon.save(static_file_name, image_file, save=True)


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0002_auto_20150207_1845'),
    ]

    operations = [
        migrations.RunPython(populate_player_icons),
    ]
