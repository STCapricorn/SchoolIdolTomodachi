# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0025_auto_20180723_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='old_art',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art (Old)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='old_art_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art (Old, Idolized)'),
            preserve_default=True,
        ),
    ]
