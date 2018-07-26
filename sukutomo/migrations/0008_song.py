# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0007_auto_20180726_0059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('d_titles', models.TextField(null=True)),
                ('romaji', models.CharField(max_length=100, null=True, verbose_name='Title (Romaji)')),
                ('cover', models.ImageField(upload_to=b'', null=True, verbose_name='Song Cover')),
                ('i_attribute', models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(0, 'Smile'), (1, 'Pure'), (2, 'Cool')])),
                ('i_unit', models.PositiveIntegerField(null=True, verbose_name='Unit', choices=[(0, "\u03bc's"), (1, b'Aqours')])),
                ('i_subunit', models.PositiveIntegerField(null=True, verbose_name='Subunit', choices=[(0, b'Printemps'), (1, b'Lily White'), (2, b'BiBi'), (3, b'CYaRon'), (4, b'AZALEA'), (5, b'Guilty Kiss'), (6, b'Saint Snow'), (7, b'A-RISE')])),
                ('c_versions', models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True)),
                ('c_locations', models.TextField(null=True, verbose_name='Locations', blank=True)),
                ('unlock', models.PositiveIntegerField(help_text='Will be displayed as "Rank __"', null=True, verbose_name='Unlock')),
                ('daily', models.CharField(max_length=100, null=True, verbose_name='Daily rotation')),
                ('b_side_master', models.BooleanField(default=False, verbose_name='MASTER')),
                ('b_side_start', models.DateTimeField(null=True, verbose_name='B-Side - Beginning')),
                ('b_side_end', models.DateTimeField(null=True, verbose_name='B-Side - End')),
                ('release', models.DateTimeField(null=True, verbose_name='Release date')),
                ('itunes_id', models.PositiveIntegerField(help_text=b'iTunes ID', null=True, verbose_name='Preview')),
                ('length', models.PositiveIntegerField(help_text='in seconds', null=True, verbose_name='Length')),
                ('bpm', models.PositiveIntegerField(null=True, verbose_name='Beats per minute')),
                ('composer', models.CharField(max_length=100, null=True, verbose_name='Composer')),
                ('lyricist', models.CharField(max_length=100, null=True, verbose_name='Lyricist')),
                ('arranger', models.CharField(max_length=100, null=True, verbose_name='Arranger')),
                ('easy_notes', models.PositiveIntegerField(null=True, verbose_name='EASY - Notes')),
                ('easy_difficulty', models.PositiveIntegerField(null=True, verbose_name='EASY - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('normal_notes', models.PositiveIntegerField(null=True, verbose_name='NORMAL - Notes')),
                ('normal_difficulty', models.PositiveIntegerField(null=True, verbose_name='NORMAL - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('hard_notes', models.PositiveIntegerField(null=True, verbose_name='HARD - Notes')),
                ('hard_difficulty', models.PositiveIntegerField(null=True, verbose_name='HARD - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('expert_notes', models.PositiveIntegerField(null=True, verbose_name='EXPERT - Notes')),
                ('expert_difficulty', models.PositiveIntegerField(null=True, verbose_name='EXPERT - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('master_notes', models.PositiveIntegerField(null=True, verbose_name='MASTER - Notes')),
                ('master_difficulty', models.PositiveIntegerField(null=True, verbose_name='MASTER - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('master_swipe', models.BooleanField(default=False, verbose_name='with SWIPE notes')),
                ('owner', models.ForeignKey(related_name='added_songs', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
