# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0007_songs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
    ]
