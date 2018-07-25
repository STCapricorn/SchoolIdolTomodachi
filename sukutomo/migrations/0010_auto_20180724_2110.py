# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0009_card_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='d_detailss',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='cards',
            field=models.ManyToManyField(related_name='event_cards', verbose_name='Featured Cards', to='sukutomo.Card'),
            preserve_default=True,
        ),
    ]
