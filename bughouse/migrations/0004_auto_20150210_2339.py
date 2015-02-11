# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0003_auto_20150207_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='black_player',
            field=models.ForeignKey(related_name='teams_as_black', on_delete=django.db.models.deletion.PROTECT, to='bughouse.Player'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='white_player',
            field=models.ForeignKey(related_name='teams_as_white', on_delete=django.db.models.deletion.PROTECT, to='bughouse.Player'),
            preserve_default=True,
        ),
    ]
