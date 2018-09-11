# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0011_auto_20180909_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='i_skill_type',
        ),
        migrations.AlterField(
            model_name='card',
            name='i_group',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost Group', choices=[(0, 'Unit'), (1, 'Subunit'), (2, 'Year')]),
            preserve_default=True,
        ),
    ]
