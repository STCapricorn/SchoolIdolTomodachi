# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0021_auto_20180721_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='idol',
            field=models.ForeignKey(related_name='card_idols', to='sukutomo.Idol', null=True),
            preserve_default=True,
        ),
    ]
