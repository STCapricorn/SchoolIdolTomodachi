# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0015_auto_20180720_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='i_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill Type', choices=[(0, 'Score Up'), (1, 'Timing Boost'), (2, 'Recovery'), (3, 'Stat Effect'), (4, 'Support')]),
            preserve_default=True,
        ),
    ]
