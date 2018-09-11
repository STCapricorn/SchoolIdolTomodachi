# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0012_auto_20180909_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='i_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill Type', choices=[(0, 'Score Up'), (1, 'Timing Boost'), (2, 'Recovery'), (3, 'Stat Effect'), (4, 'Support')]),
            preserve_default=True,
        ),
    ]
