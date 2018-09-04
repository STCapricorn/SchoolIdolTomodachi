# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0015_auto_20180807_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='color',
            field=magi.utils.ColorField(max_length=10, null=True, verbose_name='Color', blank=True),
            preserve_default=True,
        ),
    ]
