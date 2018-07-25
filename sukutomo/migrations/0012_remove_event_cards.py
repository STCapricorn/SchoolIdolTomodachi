# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0011_auto_20180724_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='cards',
        ),
    ]
