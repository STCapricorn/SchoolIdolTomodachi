# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0012_auto_20180804_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='hp',
            field=models.PositiveIntegerField(help_text='If card is not idolizable, just put HP + 1', null=True, verbose_name='HP (Idolized)'),
            preserve_default=True,
        ),
    ]
