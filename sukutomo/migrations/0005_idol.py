# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0004_idol'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='d_descriptions',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='d_favorite_foods',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='d_hobbiess',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='d_least_favorite_foods',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='d_names',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='i_school',
            field=models.PositiveIntegerField(null=True, verbose_name='School', choices=[(0, 'Chitose Bridge High School'), (1, 'Seiran High School'), (2, 'Shinonome Academy'), (3, "Shion Girls' Academy"), (4, 'Touou Academy'), (5, 'Y.G. International Academy'), (6, 'Nijigasaki High School'), (7, "Uranohoshi Girls' High School"), (8, 'Otonokizaka Academy')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='i_year',
            field=models.PositiveIntegerField(null=True, verbose_name='School year', choices=[(0, '1st Year'), (1, '2nd Year'), (2, '3rd Year')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='friend_points',
            field=models.PositiveIntegerField(help_text="Number of Friend Points you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", null=True, verbose_name='Friend Points'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='g',
            field=models.PositiveIntegerField(help_text="Number of G you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", null=True, verbose_name=b'G'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='loveca',
            field=models.PositiveIntegerField(help_text="Number of Love gems you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", null=True, verbose_name='Love gems'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='tickets',
            field=models.PositiveIntegerField(help_text="Number of Scouting Tickets you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", null=True, verbose_name=b'Scouting Tickets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='vouchers',
            field=models.PositiveIntegerField(help_text="Number of Vouchers (blue tickets) you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", null=True, verbose_name=b'Vouchers (blue tickets)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='idol',
            name='i_blood',
            field=models.PositiveIntegerField(null=True, verbose_name='Blood type', choices=[(0, b'O'), (1, b'A'), (2, b'B'), (3, b'AB')]),
            preserve_default=True,
        ),
    ]
