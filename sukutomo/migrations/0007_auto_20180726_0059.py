# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0006_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='i_os',
            field=models.PositiveIntegerField(null=True, verbose_name='Operating System', choices=[(0, b'android'), (1, b'ios')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='i_version',
            field=models.PositiveIntegerField(default=1, verbose_name='Version', choices=[(0, 'Japanese version'), (1, 'Worldwide version'), (2, 'Korean version'), (3, 'Chinese version'), (4, 'Taiwanese version')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='idol',
            name='d_favorite_foods',
            field=models.TextField(null=True, verbose_name='Favorite food'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='idol',
            name='i_school',
            field=models.PositiveIntegerField(null=True, verbose_name='School', choices=[(0, 'Chitose Bridge High School'), (1, 'Seiran High School'), (2, 'Shinonome Academy'), (3, "Shion Girls' Academy"), (4, 'Touou Academy'), (5, 'Y.G. International Academy'), (6, "Hakodate Seisen Girls' Academy"), (7, 'UTX High School'), (8, 'Nijigasaki High School'), (9, "Uranohoshi Girls' High School"), (10, 'Otonokizaka Academy')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='idol',
            name='i_year',
            field=models.PositiveIntegerField(null=True, verbose_name='School year', choices=[(0, '1st year'), (1, '2nd year'), (2, '3rd year')]),
            preserve_default=True,
        ),
    ]
