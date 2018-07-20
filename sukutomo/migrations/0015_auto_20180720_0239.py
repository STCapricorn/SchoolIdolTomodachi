# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0014_auto_20180720_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='skill',
            field=models.ForeignKey(related_name='added_skills', verbose_name='Skill', to='sukutomo.Skill', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='details',
            field=models.TextField(help_text='For every {for_every} {dependency}, there is a {chance}% chance __ |Optional variables: {unit}, {subunit}, {year}, {number}, {length}', null=True, verbose_name='Details'),
            preserve_default=True,
        ),
    ]
