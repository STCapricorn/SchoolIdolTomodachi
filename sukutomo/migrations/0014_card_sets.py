# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0013_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='sets',
            field=models.ForeignKey(related_name='added_sets', verbose_name='Sets', to='sukutomo.Set', null=True),
            preserve_default=True,
        ),
    ]
