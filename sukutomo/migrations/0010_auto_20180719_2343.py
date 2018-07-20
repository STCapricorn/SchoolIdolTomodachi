# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0009_auto_20180719_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='art',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='art_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art (Idolized)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='cool_max',
            field=models.PositiveIntegerField(null=True, verbose_name='Cool (Maximum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='cool_max_idol',
            field=models.PositiveIntegerField(null=True, verbose_name='Cool (Idolized, Maximum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='cool_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Cool (Minimum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='hp',
            field=models.PositiveIntegerField(null=True, verbose_name='HP (Unidolized)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='i_center',
            field=models.PositiveIntegerField(null=True, verbose_name='Center Skill', choices=[(0, 'Princess'), (1, 'Angel'), (2, 'Empress'), (3, 'Star'), (4, 'Heart'), (5, 'Power'), (6, 'Energy')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='icon',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='icon_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon (Idolized)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='image_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image (Idolized)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='pure_max',
            field=models.PositiveIntegerField(null=True, verbose_name='Pure (Maximum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='pure_max_idol',
            field=models.PositiveIntegerField(null=True, verbose_name='Pure (Idolized, Maximum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='pure_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Pure (Minimum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='smile_max',
            field=models.PositiveIntegerField(null=True, verbose_name='Smile (Maximum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='smile_max_idol',
            field=models.PositiveIntegerField(null=True, verbose_name='Smile (Idolized, Maximum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='smile_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Smile (Minimum)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='transparent',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Transparent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='transparent_idol',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Transparent (Idolized)'),
            preserve_default=True,
        ),
    ]
