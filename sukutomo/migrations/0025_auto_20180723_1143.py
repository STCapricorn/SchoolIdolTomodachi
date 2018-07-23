# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0024_auto_20180722_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='old_icon',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon (Old)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='old_icon_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon (Old, Idolized)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='old_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image (Old)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='old_image_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image (Old, Idolized)'),
            preserve_default=True,
        ),
    ]
