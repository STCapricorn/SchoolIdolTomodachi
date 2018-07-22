# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0018_auto_20180720_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='d_detailss',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='i_os',
            field=models.PositiveIntegerField(null=True, verbose_name='Operating System', choices=[(0, b'android'), (1, b'ios')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_center',
            field=models.PositiveIntegerField(null=True, verbose_name='Center Skill', choices=[(0, 'Princess'), (1, 'Angel'), (2, 'Empress'), (3, 'Star'), (4, 'Heart'), (5, 'Energy'), (6, 'Power')]),
            preserve_default=True,
        ),
    ]
