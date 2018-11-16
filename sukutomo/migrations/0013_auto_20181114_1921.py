# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0012_auto_20181114_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='c_locations',
            field=models.TextField(null=True, verbose_name='Location', blank=True),
            preserve_default=True,
        ),
    ]
