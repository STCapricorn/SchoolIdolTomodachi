# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0009_cardsetskill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='hp',
            field=models.PositiveIntegerField(null=True, verbose_name='HP (Idolized)'),
            preserve_default=True,
        ),
    ]
