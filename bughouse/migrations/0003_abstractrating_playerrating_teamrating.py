# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bughouse', '0002_auto_20150129_0217'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerRating',
            fields=[
                ('abstractrating_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bughouse.AbstractRating')),
                ('game', models.ForeignKey(related_name='player_ratings', to='bughouse.Game')),
                ('player', models.ForeignKey(related_name='ratings', to='bughouse.Player')),
            ],
            options={
            },
            bases=('bughouse.abstractrating',),
        ),
        migrations.CreateModel(
            name='TeamRating',
            fields=[
                ('abstractrating_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bughouse.AbstractRating')),
                ('game', models.ForeignKey(related_name='team_ratings', to='bughouse.Game')),
                ('team', models.ForeignKey(related_name='ratings', to='bughouse.Team')),
            ],
            options={
            },
            bases=('bughouse.abstractrating',),
        ),
    ]
