# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0008_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='d_skill_names',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='i_attribute',
            field=models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(0, 'Smile'), (1, 'Pure'), (2, 'Cool'), (3, 'All')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='i_rarity',
            field=models.PositiveIntegerField(null=True, verbose_name='Rarity', choices=[(0, b'N'), (1, b'R'), (2, b'SR'), (3, b'SSR'), (4, b'UR')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='limited',
            field=models.BooleanField(default=False, verbose_name='Limited'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='promo',
            field=models.BooleanField(default=False, verbose_name='Promo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='release',
            field=models.DateTimeField(null=True, verbose_name='Release date'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='skill_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Skill name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='support',
            field=models.BooleanField(default=False, verbose_name='Support'),
            preserve_default=True,
        ),
    ]
