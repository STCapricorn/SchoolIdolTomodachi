# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0013_auto_20181114_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='japanese_title',
            field=models.CharField(default='a', max_length=100, verbose_name='Title (Japanese)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=100, null=True, verbose_name='Title'),
            preserve_default=True,
        ),
    ]
