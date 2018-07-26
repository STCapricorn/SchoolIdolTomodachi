# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0017_remove_card_i_sets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idol',
            name='i_school',
            field=models.PositiveIntegerField(null=True, verbose_name='School', choices=[(0, 'Chitose Bridge High School'), (1, 'Seiran High School'), (2, 'Shinonome Academy'), (3, "Shion Girls' Academy"), (4, 'Touou Academy'), (5, 'Y.G. International Academy'), (6, "Hakodate Seisen Girls' Academy"), (7, 'UTX High School'), (8, 'Nijigasaki High School'), (9, "Uranohoshi Girls' High School"), (10, 'Otonokizaka Academy')]),
            preserve_default=True,
        ),
    ]
