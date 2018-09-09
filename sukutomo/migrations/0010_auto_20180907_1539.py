# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0009_cardsetskill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='support',
        ),
        migrations.AddField(
            model_name='card',
            name='i_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill Type', choices=[(0, 'Score Up'), (1, 'Timing Boost'), (2, 'Recovery'), (3, 'Stat Effect'), (4, 'Support')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_group',
            field=models.PositiveIntegerField(null=True, verbose_name='Center Boost', choices=[(0, 'Unit'), (1, 'Subunit'), (2, 'Year')]),
            preserve_default=True,
        ),
    ]
