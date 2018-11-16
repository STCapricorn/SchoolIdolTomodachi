# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0006_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('japanese_title', models.CharField(max_length=100, verbose_name='Title (Japanese)')),
                ('d_titles', models.TextField(null=True)),
                ('romaji', models.CharField(max_length=100, null=True, verbose_name='Title (Romaji)')),
                ('cover', models.ImageField(upload_to=magi.utils.uploadItem(b's'), null=True, verbose_name='Song Cover')),
                ('i_attribute', models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(0, 'Smile'), (1, 'Pure'), (2, 'Cool')])),
                ('i_unit', models.PositiveIntegerField(null=True, verbose_name='Unit', choices=[(0, "\u03bc's"), (1, b'Aqours')])),
                ('i_subunit', models.PositiveIntegerField(null=True, verbose_name='Subunit', choices=[(0, b'Printemps'), (1, b'Lily White'), (2, b'BiBi'), (3, b'CYaRon'), (4, b'AZALEA'), (5, b'Guilty Kiss'), (6, b'Saint Snow'), (7, b'A-RISE')])),
                ('c_versions', models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True)),
                ('c_locations', models.TextField(null=True, verbose_name='Location', blank=True)),
                ('unlock', models.PositiveIntegerField(help_text=b'Will be displayed as "Rank __"', null=True, verbose_name='Unlock')),
                ('daily', models.CharField(max_length=100, null=True, verbose_name='Daily rotation')),
                ('b_side_master', models.BooleanField(default=False, verbose_name='MASTER')),
                ('b_side_start', models.DateTimeField(null=True, verbose_name='B-Side - Beginning')),
                ('b_side_end', models.DateTimeField(null=True, verbose_name='B-Side - End')),
                ('release', models.DateTimeField(null=True, verbose_name='Release date')),
                ('itunes_id', models.PositiveIntegerField(help_text=b'iTunes ID', null=True, verbose_name='Preview')),
                ('length', models.PositiveIntegerField(help_text=b'in seconds', null=True, verbose_name='Length')),
                ('bpm', models.PositiveIntegerField(null=True, verbose_name='Beats per minute')),
                ('composer', models.CharField(max_length=100, null=True, verbose_name='Composer')),
                ('lyricist', models.CharField(max_length=100, null=True, verbose_name='Lyricist')),
                ('arranger', models.CharField(max_length=100, null=True, verbose_name='Arranger')),
                ('easy_notes', models.PositiveIntegerField(null=True, verbose_name='EASY notes')),
                ('easy_rating', models.PositiveIntegerField(null=True, verbose_name='EASY &#9734 rating', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)])),
                ('normal_notes', models.PositiveIntegerField(null=True, verbose_name='NORMAL notes')),
                ('normal_rating', models.PositiveIntegerField(null=True, verbose_name='NORMAL &#9734 rating', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)])),
                ('hard_notes', models.PositiveIntegerField(null=True, verbose_name='HARD notes')),
                ('hard_rating', models.PositiveIntegerField(null=True, verbose_name='HARD &#9734 rating', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)])),
                ('expert_notes', models.PositiveIntegerField(null=True, verbose_name='EXPERT notes')),
                ('expert_rating', models.PositiveIntegerField(null=True, verbose_name='EXPERT &#9734 rating', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)])),
                ('master_notes', models.PositiveIntegerField(null=True, verbose_name='MASTER notes')),
                ('master_rating', models.PositiveIntegerField(null=True, verbose_name='MASTER &#9734 rating', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(15)])),
                ('master_swipe', models.BooleanField(default=False, verbose_name='with SWIPE notes')),
                ('owner', models.ForeignKey(related_name='added_songs', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='event',
            name='banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='cn_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='jp_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='kr_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tw_banner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='ww_banner',
        ),
        migrations.AddField(
            model_name='event',
            name='cn_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Chinese version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='jp_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Japanese version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='kr_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Korean version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='tw_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Taiwanese version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='ww_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Worldwide version-Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='color',
            field=magi.utils.ColorField(max_length=10, null=True, verbose_name='Color', blank=True),
            preserve_default=True,
        ),
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
            name='favorite_food',
            field=models.CharField(max_length=100, null=True, verbose_name='Liked food'),
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
        migrations.AlterField(
            model_name='idol',
            name='least_favorite_food',
            field=models.CharField(max_length=100, null=True, verbose_name='Disliked food'),
            preserve_default=True,
        ),
    ]
