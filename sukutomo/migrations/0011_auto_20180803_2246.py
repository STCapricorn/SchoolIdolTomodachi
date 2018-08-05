# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0010_auto_20180803_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='i_rarity',
            field=models.PositiveIntegerField(null=True, verbose_name='Rarity', choices=[(0, {b'max': 30, b'max_idol': 40}), (1, {b'max': 40, b'max_idol': 60}), (2, {b'max': 60, b'max_idol': 80}), (3, {b'max': 70, b'max_idol': 90}), (4, {b'max': 80, b'max_idol': 100})]),
            preserve_default=True,
        ),
    ]
