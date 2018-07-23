# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0022_auto_20180721_1404'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='d_skill_names',
            new_name='d_names',
        ),
        migrations.RemoveField(
            model_name='card',
            name='skill_name',
        ),
    ]
