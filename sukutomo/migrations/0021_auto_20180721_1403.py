# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0020_auto_20180721_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='idol',
            field=models.ForeignKey(related_name='card_idols', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
