# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 29, 2, 17, 2, 615378), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 29, 2, 17, 7, 301310), auto_now=True),
            preserve_default=False,
        ),
    ]
