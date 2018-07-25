# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0014_card_sets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='sets',
            field=models.ForeignKey(related_name='sets', verbose_name='Sets', to='sukutomo.Set', null=True),
            preserve_default=True,
        ),
    ]
