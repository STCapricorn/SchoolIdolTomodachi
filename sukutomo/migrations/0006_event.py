# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0005_idol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('d_titles', models.TextField(null=True)),
                ('banner', models.ImageField(upload_to=b'', null=True, verbose_name='Banner')),
                ('i_type', models.PositiveIntegerField(null=True, verbose_name='Event type', choices=[(0, 'Token'), (1, 'Score Match'), (2, 'Medley Festival'), (3, 'Challenge Festival'), (4, 'Adventure Stroll'), (5, 'Friendly Match')])),
                ('i_unit', models.PositiveIntegerField(null=True, verbose_name='Unit', choices=[(0, "\u03bc's"), (1, b'Aqours')])),
                ('c_versions', models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True)),
                ('jp_banner', models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Japanese version-Banner')),
                ('jp_start_date', models.DateTimeField(null=True, verbose_name='Japanese version - Beginning')),
                ('jp_end_date', models.DateTimeField(null=True, verbose_name='Japanese version - End')),
                ('ww_banner', models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Worldwide version-Banner')),
                ('ww_start_date', models.DateTimeField(null=True, verbose_name='Worldwide version - Beginning')),
                ('ww_end_date', models.DateTimeField(null=True, verbose_name='Worldwide version - End')),
                ('tw_banner', models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Taiwanese version-Banner')),
                ('tw_start_date', models.DateTimeField(null=True, verbose_name='Taiwanese version - Beginning')),
                ('tw_end_date', models.DateTimeField(null=True, verbose_name='Taiwanese version - End')),
                ('kr_banner', models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Korean version-Banner')),
                ('kr_start_date', models.DateTimeField(null=True, verbose_name='Korean version - Beginning')),
                ('kr_end_date', models.DateTimeField(null=True, verbose_name='Korean version - End')),
                ('cn_banner', models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Chinese version-Banner')),
                ('cn_start_date', models.DateTimeField(null=True, verbose_name='Chinese version - Beginning')),
                ('cn_end_date', models.DateTimeField(null=True, verbose_name='Chinese version - End')),
                ('owner', models.ForeignKey(related_name='added_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
