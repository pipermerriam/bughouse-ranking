# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0005_auto_20150211_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerrating',
            name='key',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamrating',
            name='key',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
