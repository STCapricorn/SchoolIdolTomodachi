# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0010_auto_20180907_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='set',
            old_name='i_unit_type',
            new_name='i_unit',
        ),
    ]
