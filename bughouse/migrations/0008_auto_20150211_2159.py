# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0007_auto_20150211_2026'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='playerrating',
            unique_together=set([('game', 'player', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='teamrating',
            unique_together=set([('game', 'team', 'key')]),
        ),
    ]
