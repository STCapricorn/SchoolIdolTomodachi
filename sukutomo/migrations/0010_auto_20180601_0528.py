# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0009_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='arranger',
            field=models.CharField(max_length=100, null=True, verbose_name='Arranger'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='bpm',
            field=models.PositiveIntegerField(null=True, verbose_name='Beats per minute'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='composer',
            field=models.CharField(max_length=100, null=True, verbose_name='Composer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='cover',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='Song Cover'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='easy_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Easy - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='easy_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='Easy - Notes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='expert_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Expert - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='expert_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='Expert - Notes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='hard_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Hard - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='hard_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='Hard - Notes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='i_attribute',
            field=models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(0, 'Smile'), (1, 'Pure'), (2, 'Cool'), (3, 'All')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='i_unit',
            field=models.PositiveIntegerField(null=True, verbose_name='Unit', choices=[(0, "\u03bc's"), (1, b'Aqours')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='itunes_id',
            field=models.PositiveIntegerField(help_text=b'iTunes ID', null=True, verbose_name='Preview'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='length',
            field=models.PositiveIntegerField(null=True, verbose_name='Length'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='lyricist',
            field=models.CharField(max_length=100, null=True, verbose_name='Lyricist'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='master_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Master - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='master_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='Master - Notes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='normal_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Normal - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='normal_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='Normal - Notes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='romaji',
            field=models.CharField(max_length=100, null=True, verbose_name='Title (Romaji)'),
            preserve_default=True,
        ),
    ]
