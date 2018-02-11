# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-11 20:23
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('my_simple_survey', '0003_player_still_confidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='still_confidence',
            field=otree.db.models.StringField(choices=[(1, 'Not confident at all'), (2, ''), (3, ''), (4, 'Somewhat confident'), (5, ''), (6, ''), (7, 'Very confident')], max_length=10000, null=True),
        ),
    ]
