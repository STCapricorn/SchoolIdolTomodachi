# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0012_auto_20180720_0158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('d_names', models.TextField(null=True)),
                ('i_skill_type', models.PositiveIntegerField(null=True, verbose_name='Skill Type', choices=[(0, 'Score Up'), (1, 'Perfect Lock'), (2, 'Healer'), (3, 'Stat Boost'), (4, 'Support')])),
                ('for_every', models.PositiveIntegerField(help_text='For every __ seconds', verbose_name=b'chance time')),
                ('chance', models.PositiveIntegerField(help_text='there is a __% chance', verbose_name=b'chance %')),
                ('number', models.BooleanField(default=False, verbose_name=b'number')),
                ('length', models.PositiveIntegerField(default=False, verbose_name=b'length')),
                ('details', models.TextField(help_text='For every {for_every} {dependency}, there is a __% chance {details}', null=True, verbose_name='Details')),
                ('owner', models.ForeignKey(related_name='added_skills', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
