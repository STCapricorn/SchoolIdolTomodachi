# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0013_auto_20180806_0625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='banner',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='card',
            name='art_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'c'), null=True, verbose_name='Art (Idolized)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='old_art_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'c'), null=True, verbose_name='Art (Old, Idolized)'),
            preserve_default=True,
        ),
    ]
