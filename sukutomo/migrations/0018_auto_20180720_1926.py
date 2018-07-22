# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0017_auto_20180720_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='details',
            field=models.TextField(help_text='For every {for_every} {dependency}, there is a {chance}% chance __ |Optional variables: {unit}, {subunit}, {year}, {number}, {length}', null=True, verbose_name='Details'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='i_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill Type', choices=[(0, 'Score Up'), (1, 'Timing Boost'), (2, 'Recovery'), (3, 'Stat Effect'), (4, 'Support')]),
            preserve_default=True,
        ),
    ]
