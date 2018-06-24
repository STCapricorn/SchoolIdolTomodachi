# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0007_auto_20180623_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='b_side_master',
            field=models.BooleanField(default=False, verbose_name='Master'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='b_side_start',
            field=models.DateTimeField(null=True, verbose_name='B-Side Beginning'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='easy_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='EASY - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='easy_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='EASY - Notes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='expert_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='EXPERT - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='expert_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='EXPERT - Notes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='hard_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='HARD - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='hard_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='HARD - Notes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='i_attribute',
            field=models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(0, 'Smile'), (1, 'Pure'), (2, 'Cool')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='length',
            field=models.PositiveIntegerField(help_text='in seconds', null=True, verbose_name='Length'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='master_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='MASTER - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='master_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='MASTER - Notes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='master_swipe',
            field=models.BooleanField(default=False, verbose_name='with SWIPE notes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='normal_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='NORMAL - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='normal_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='NORMAL - Notes'),
            preserve_default=True,
        ),
    ]
