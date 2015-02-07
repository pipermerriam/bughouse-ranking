# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='icon',
            field=models.ImageField(upload_to=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playerrating',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teamrating',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=True,
        ),
    ]
