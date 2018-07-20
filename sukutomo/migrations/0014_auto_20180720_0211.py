# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0013_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='chance',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='for_every',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='length',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='number',
        ),
        migrations.AlterField(
            model_name='skill',
            name='details',
            field=models.TextField(help_text='For every {for_every} {dependency}, there is a __% chance {details}\n\nOther optional variables: {unit}, {subunit}, {year}, {number}, {length}', null=True, verbose_name='Details'),
            preserve_default=True,
        ),
    ]
