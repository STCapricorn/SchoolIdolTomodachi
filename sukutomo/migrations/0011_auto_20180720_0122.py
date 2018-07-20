# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0010_auto_20180719_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='boost_percent',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost Percentage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='chance',
            field=models.PositiveIntegerField(help_text='there is a __% chance', null=True, verbose_name='Activation Chance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='for_every',
            field=models.PositiveIntegerField(help_text='For every __ seconds', null=True, verbose_name='Rate of Activation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='i_group',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost Group', choices=[(0, 'Unit'), (1, 'Subunit'), (2, 'Year')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='length',
            field=models.PositiveIntegerField(null=True, verbose_name=b'{length}'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='number',
            field=models.PositiveIntegerField(null=True, verbose_name=b'{number}'),
            preserve_default=True,
        ),
    ]
