# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0007_auto_20180717_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='b_side_end',
            field=models.DateTimeField(null=True, verbose_name='B-Side - End'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='b_side_start',
            field=models.DateTimeField(null=True, verbose_name='B-Side - Beginning'),
            preserve_default=True,
        ),
    ]
