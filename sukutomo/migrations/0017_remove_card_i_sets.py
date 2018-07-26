# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0016_card_i_sets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='i_sets',
        ),
    ]
