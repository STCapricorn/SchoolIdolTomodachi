# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0010_auto_20180724_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cards',
            field=models.ManyToManyField(related_name='event_cards', null=True, verbose_name='Featured Cards', to='sukutomo.Card'),
            preserve_default=True,
        ),
    ]
