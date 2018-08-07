# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0014_auto_20180807_0927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='cn_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='jp_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='kr_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tw_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='ww_banner',
        ),
        migrations.AddField(
            model_name='event',
            name='cn_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Chinese version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='jp_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Japanese version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='kr_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Korean version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='tw_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Taiwanese version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='ww_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Worldwide version-Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Image'),
            preserve_default=True,
        ),
    ]
