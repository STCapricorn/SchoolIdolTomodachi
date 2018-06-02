# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0010_auto_20180601_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='release',
            field=models.DateTimeField(null=True, verbose_name='Release date'),
            preserve_default=True,
        ),
    ]
