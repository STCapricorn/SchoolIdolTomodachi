# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sukutomo', '0007_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card_id', models.PositiveIntegerField(unique=True, verbose_name='ID')),
                ('i_rarity', models.PositiveIntegerField(null=True, verbose_name='Rarity', choices=[(0, b'N'), (1, b'R'), (2, b'SR'), (3, b'SSR'), (4, b'UR')])),
                ('limited', models.BooleanField(default=False, verbose_name='Limited')),
                ('promo', models.BooleanField(default=False, verbose_name='Promo')),
                ('support', models.BooleanField(default=False, verbose_name='Support')),
                ('i_attribute', models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(0, 'Smile'), (1, 'Pure'), (2, 'Cool'), (3, 'All')])),
                ('c_versions', models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True)),
                ('release', models.DateTimeField(null=True, verbose_name='Release date')),
                ('skill_name', models.CharField(max_length=100, null=True, verbose_name='Skill name')),
                ('d_skill_names', models.TextField(null=True)),
                ('rate', models.PositiveIntegerField(help_text='Every __ {dependency}', null=True, verbose_name='Rate of Activation')),
                ('i_dependency', models.PositiveIntegerField(null=True, verbose_name='Dependency', choices=[(0, 'notes'), (1, b'PERFECTs'), (2, 'seconds'), (3, 'x combo')])),
                ('chance', models.PositiveIntegerField(help_text='there is a __% chance', null=True, verbose_name='% Chance')),
                ('number', models.PositiveIntegerField(null=True, verbose_name=b'{number}')),
                ('length', models.PositiveIntegerField(null=True, verbose_name=b'{length}')),
                ('i_center', models.PositiveIntegerField(null=True, verbose_name='Center Skill', choices=[(0, 'Princess'), (1, 'Angel'), (2, 'Empress'), (3, 'Star'), (4, 'Heart'), (5, 'Energy'), (6, 'Power')])),
                ('i_group', models.PositiveIntegerField(null=True, verbose_name='Boost Group', choices=[(0, 'Unit'), (1, 'Subunit'), (2, 'Year')])),
                ('boost_percent', models.PositiveIntegerField(null=True, verbose_name='Boost Percentage')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image')),
                ('image_idol', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image (Idolized)')),
                ('old_image', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image (Old)')),
                ('old_image_idol', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image (Old, Idolized)')),
                ('icon', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon')),
                ('icon_idol', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon (Idolized)')),
                ('old_icon', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon (Old)')),
                ('old_icon_idol', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Icon (Old, Idolized)')),
                ('transparent', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Transparent')),
                ('transparent_idol', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Transparent (Idolized)')),
                ('art', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art')),
                ('art_idol', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art (Idolized)')),
                ('old_art', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art (Old)')),
                ('old_art_idol', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Art (Old, Idolized)')),
                ('smile_min', models.PositiveIntegerField(null=True, verbose_name='Smile (Minimum)')),
                ('smile_max', models.PositiveIntegerField(null=True, verbose_name='Smile (Maximum)')),
                ('smile_max_idol', models.PositiveIntegerField(null=True, verbose_name='Smile (Idolized, Maximum)')),
                ('pure_min', models.PositiveIntegerField(null=True, verbose_name='Pure (Minimum)')),
                ('pure_max', models.PositiveIntegerField(null=True, verbose_name='Pure (Maximum)')),
                ('pure_max_idol', models.PositiveIntegerField(null=True, verbose_name='Pure (Idolized, Maximum)')),
                ('cool_min', models.PositiveIntegerField(null=True, verbose_name='Cool (Minimum)')),
                ('cool_max', models.PositiveIntegerField(null=True, verbose_name='Cool (Maximum)')),
                ('cool_max_idol', models.PositiveIntegerField(null=True, verbose_name='Cool (Idolized, Maximum)')),
                ('hp', models.PositiveIntegerField(null=True, verbose_name='HP (Unidolized)')),
                ('idol', models.ForeignKey(related_name='card_idols', to='sukutomo.Idol', null=True)),
                ('owner', models.ForeignKey(related_name='added_cards', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('d_names', models.TextField(null=True)),
                ('i_skill_type', models.PositiveIntegerField(null=True, verbose_name='Skill Type', choices=[(0, 'Score Up'), (1, 'Timing Boost'), (2, 'Recovery'), (3, 'Stat Effect'), (4, 'Support')])),
                ('details', models.TextField(help_text='Optional variables: {rate}, {dependency}, {chance}, {unit}, {subunit}, {year}, {number}, {length}', null=True, verbose_name='Details')),
                ('d_detailss', models.TextField(null=True)),
                ('owner', models.ForeignKey(related_name='added_skills', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='skill',
            field=models.ForeignKey(related_name='added_skills', verbose_name='Skill', to='sukutomo.Skill', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='i_os',
            field=models.PositiveIntegerField(null=True, verbose_name='Operating System', choices=[(0, b'android'), (1, b'ios')]),
            preserve_default=True,
        ),
    ]
