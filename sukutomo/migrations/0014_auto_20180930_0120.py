# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0013_card_i_skill_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='card_id',
        ),
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.PositiveIntegerField(unique=True, serialize=False, verbose_name='ID', primary_key=True),
            preserve_default=True,
        ),
    ]
