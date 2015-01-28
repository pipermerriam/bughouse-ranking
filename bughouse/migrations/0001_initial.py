# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('losing_color', models.CharField(max_length=20, choices=[(b'white', b'White'), (b'black', b'Black')])),
                ('loss_type', models.CharField(default=b'unknown', max_length=20, blank=True, choices=[(b'checkmate', b'Checkmate'), (b'time', b'Time'), (b'swindle', b'Swindle'), (b'imminent-death', b'Imminent Death')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('black_player', models.ForeignKey(related_name='teams_as_black', to='bughouse.Player')),
                ('white_player', models.ForeignKey(related_name='teams_as_white', to='bughouse.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('white_player', 'black_player')]),
        ),
        migrations.AddField(
            model_name='game',
            name='losing_team',
            field=models.ForeignKey(related_name='game_losses', to='bughouse.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='winning_team',
            field=models.ForeignKey(related_name='game_wins', to='bughouse.Team'),
            preserve_default=True,
        ),
    ]
