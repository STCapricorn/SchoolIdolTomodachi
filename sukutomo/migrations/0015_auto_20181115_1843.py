# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0014_auto_20181115_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='romaji',
            new_name='japanese_romaji',
        ),
    ]
