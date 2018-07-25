# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0012_remove_event_cards'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100, verbose_name='Title')),
                ('d_titles', models.TextField(null=True)),
                ('i_set_type', models.PositiveIntegerField(null=True, verbose_name='Type', choices=[(0, 'Gacha'), (1, 'Event')])),
                ('i_unit_type', models.PositiveIntegerField(null=True, verbose_name='Unit', choices=[(0, "\u03bc's"), (1, b'Aqours')])),
                ('owner', models.ForeignKey(related_name='added_sets', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
