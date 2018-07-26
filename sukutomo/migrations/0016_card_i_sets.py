# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0015_auto_20180725_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='i_sets',
            field=models.PositiveIntegerField(null=True, verbose_name='Set', choices=[(0, b's'), (1, b'e'), (2, b't'), (3, b's')]),
            preserve_default=True,
        ),
    ]
