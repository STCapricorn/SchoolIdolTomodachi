# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0018_auto_20180725_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='sets',
            new_name='in_set',
        ),
    ]
