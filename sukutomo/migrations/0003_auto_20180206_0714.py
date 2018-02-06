# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0002_auto_20171221_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='default_tab',
            field=models.CharField(max_length=100, null=True, verbose_name='Default tab'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='nickname',
            field=models.CharField(help_text="Give a nickname to your account to easily differentiate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start date'),
            preserve_default=True,
        ),
    ]
