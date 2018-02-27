# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0003_auto_20180206_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('japanese_name', models.CharField(max_length=100, null=True, verbose_name='Name (Japanese)')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image')),
                ('i_attribute', models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(0, 'Smile'), (1, 'Pure'), (2, 'Cool'), (3, 'All')])),
                ('i_unit', models.PositiveIntegerField(null=True, verbose_name='Unit', choices=[(0, "\u03bc's"), (1, b'Aqours')])),
                ('i_subunit', models.PositiveIntegerField(null=True, verbose_name='Subunit', choices=[(0, b'Printemps'), (1, b'Lily White'), (2, b'BiBi'), (3, b'CYaRon'), (4, b'AZALEA'), (5, b'Guilty Kiss'), (6, b'Saint Snow'), (7, b'A-RISE')])),
                ('age', models.PositiveIntegerField(null=True, verbose_name='Age')),
                ('birthday', models.DateField(null=True, verbose_name='Birthday')),
                ('i_astrological_sign', models.PositiveIntegerField(null=True, verbose_name='Astrological sign', choices=[(0, 'Leo'), (1, 'Aries'), (2, 'Libra'), (3, 'Virgo'), (4, 'Scorpio'), (5, 'Capricorn'), (6, 'Pisces'), (7, 'Gemini'), (8, 'Cancer'), (9, 'Sagittarius'), (10, 'Aquarius'), (11, 'Taurus')])),
                ('i_blood', models.PositiveIntegerField(null=True, verbose_name='Blood', choices=[(0, b'O'), (1, b'A'), (2, b'B'), (3, b'AB')])),
                ('height', models.PositiveIntegerField(default=None, null=True, verbose_name='Height')),
                ('bust', models.PositiveIntegerField(null=True, verbose_name='Bust')),
                ('waist', models.PositiveIntegerField(null=True, verbose_name='Waist')),
                ('hips', models.PositiveIntegerField(null=True, verbose_name='Hips')),
                ('hobbies', models.CharField(max_length=100, null=True, verbose_name='Hobbies')),
                ('favorite_food', models.CharField(max_length=100, null=True, verbose_name='Favorite food')),
                ('least_favorite_food', models.CharField(max_length=100, null=True, verbose_name='Least favorite food')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(related_name='added_idols', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
