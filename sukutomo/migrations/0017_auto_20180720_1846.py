# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0016_auto_20180720_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='dependency',
        ),
        migrations.RemoveField(
            model_name='card',
            name='for_every',
        ),
        migrations.AddField(
            model_name='card',
            name='i_dependency',
            field=models.PositiveIntegerField(null=True, verbose_name='Dependency', choices=[(0, 'notes'), (1, b'PERFECTs'), (2, 'seconds'), (3, 'x combo')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='rate',
            field=models.PositiveIntegerField(help_text='Every __ {dependency}', null=True, verbose_name='Rate of Activation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='chance',
            field=models.PositiveIntegerField(help_text='there is a __% chance', null=True, verbose_name='% Chance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='details',
            field=models.TextField(default=b'None', help_text='For every {for_every} {dependency}, there is a {chance}% chance __ |Optional variables: {unit}, {subunit}, {year}, {number}, {length}', verbose_name='Details'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='i_skill_type',
            field=models.PositiveIntegerField(default=1, verbose_name='Skill Type', choices=[(0, 'Score Up'), (1, 'Timing Boost'), (2, 'Recovery'), (3, 'Stat Effect'), (4, 'Support')]),
            preserve_default=True,
        ),
    ]
