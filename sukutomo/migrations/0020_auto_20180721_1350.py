# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0019_auto_20180720_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='details',
            field=models.TextField(help_text='Optional variables: {rate}, {dependency}, {chance}, {unit}, {subunit}, {year}, {number}, {length}', null=True, verbose_name='Details'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
