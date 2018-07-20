# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0011_auto_20180720_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='dependency',
            field=models.CharField(help_text='For every {for_every} __', max_length=100, null=True, verbose_name='Dependency'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='for_every',
            field=models.PositiveIntegerField(help_text='For every __ {dependency}', null=True, verbose_name='Rate of Activation'),
            preserve_default=True,
        ),
    ]
