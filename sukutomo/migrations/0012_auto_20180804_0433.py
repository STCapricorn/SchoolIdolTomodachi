# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0011_auto_20180803_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='i_rarity',
            field=models.PositiveIntegerField(null=True, verbose_name='Rarity', choices=[(0, b'N'), (1, b'R'), (2, b'SR'), (3, b'SSR'), (4, b'UR')]),
            preserve_default=True,
        ),
    ]
