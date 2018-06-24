# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0007_auto_20180623_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='b_side_master',
            field=models.BooleanField(default=False, verbose_name='MASTER'),
            preserve_default=True,
        ),
    ]
