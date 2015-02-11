# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0004_auto_20150210_2339'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='playerrating',
            unique_together=set([('game', 'player')]),
        ),
        migrations.AlterUniqueTogether(
            name='teamrating',
            unique_together=set([('game', 'team')]),
        ),
    ]
