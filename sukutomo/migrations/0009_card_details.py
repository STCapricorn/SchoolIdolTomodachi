# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0008_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='details',
            field=models.TextField(null=True, verbose_name='Details'),
            preserve_default=True,
        ),
    ]
