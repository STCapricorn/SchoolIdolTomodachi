# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0023_auto_20180722_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='d_names',
            new_name='d_skill_names',
        ),
        migrations.AddField(
            model_name='card',
            name='skill_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Skill name'),
            preserve_default=True,
        ),
    ]
