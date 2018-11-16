# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.translation import string_concat
from magi import settings
from magi.item_model import getInfoFromChoices
from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection, PrizeCollection as _PrizeCollection, StaffConfigurationCollection as _StaffConfigurationCollection
from magi.utils import staticImageURL, CuteFormType, CuteFormTransform, custom_item_template, toCountDown, torfc2822, setSubField, jsv, FAVORITE_CHARACTERS_IMAGES
from sukutomo import forms, models
from sukutomo.utils import generateDifficulty, subUnitMergeCuteForm

############################################################
# Prize Collection

class PrizeCollection(_PrizeCollection):
    enabled = True

############################################################
# StaffConfiguration Collection

class StaffConfigurationCollection(_StaffConfigurationCollection):
    enabled = True

############################################################
# Account Collection

class AccountCollection(_AccountCollection):
    form_class = forms.AccountForm
    navbar_link_list = 'community'

    filter_cuteform = {
        'accept_friend_requests': {
            'type': CuteFormType.YesNo,
        },
        'i_play_with': {
            'to_cuteform': lambda k, v: models.Account.PLAY_WITH[models.Account.get_reverse_i('play_with', k)]['icon'],
            'transform': CuteFormTransform.FlaticonWithText,
        },
        'i_version': {
            'to_cuteform': lambda k, v: models.Account.VERSIONS[models.Account.get_reverse_i('version', k)]['image'],
            'image_folder': 'language',
            'transform': CuteFormTransform.ImagePath,
        },
        'i_os': {
            'transform': CuteFormTransform.FlaticonWithText,
        },
    }

    class ListView(_AccountCollection.ListView):
        pass

############################################################
# Idols Collection

IDOLS_ICONS = {
    'name': 'id', 'japanese_name': 'id', 'school': 'school', 'year': 'education', 'age': 'scoreup',
    'birthday': 'birthday', 'height': 'measurements', 'blood': 'hp', 'bust': 'measurements',
    'waist': 'measurements', 'hips': 'measurements', 'color': 'palette', 'hobbies': 'hobbies',
    'favorite_food': 'food-like', 'least_favorite_food' : 'food-dislike', 'description': 'author',
}

IDOL_ORDER = [
    'image', 'name', 'attribute', 'unit', 'subunit', 'school',
    'year', 'astrological_sign', 'birthday', 'age', 'blood', 'measurements', 'color',
    'hobbies', 'favorite_food', 'least_favorite_food', 'description',
]

IDOLS_CUTEFORM = {
    'i_unit': {
    },
    'i_subunit': {
    },
    'sub_unit': {
        'to_cuteform': lambda k, v: (
            staticImageURL(k, folder='i_unit', extension='png') if float(k) - 2 < 0 else
            staticImageURL(int(k) - 2, folder='i_subunit', extension='png')
            ),
        'title': _('Unit'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'i_attribute': {
    },
    'i_year': {
        'type': CuteFormType.HTML,
    },
    'i_astrological_sign': {
    },
    'i_blood': {
        'type': CuteFormType.HTML,
    },
}

class IdolCollection(MagiCollection):
    queryset = models.Idol.objects.all()
    title = _('Idol')
    plural_title = _('Idols')
    multipart = True
    form_class = forms.IdolForm
    reportable = False
    blockable = False
    translated_fields = ('name', 'hobbies', 'favorite_food', 'least_favorite_food', 'description', )
    icon = 'idol'
    navbar_link_list = 'lovelive'

    def to_fields(self, view, item, *args, **kwargs):

        fields = super(IdolCollection, self).to_fields(view, item, *args, icons=IDOLS_ICONS,  images={
                'attribute': staticImageURL(item.i_attribute, folder='i_attribute', extension='png'),
                'unit': staticImageURL(item.i_unit, folder='i_unit', extension='png'),
                'subunit': staticImageURL(item.i_subunit, folder='i_subunit', extension='png'),
                'astrological_sign': staticImageURL(item.i_astrological_sign, folder='i_astrological_sign', extension='png'),
        }, **kwargs)

        if item.japanese_name and get_language() == 'ja':
            setSubField(fields, 'name', key='value', value=item.japanese_name)

        setSubField(fields, 'birthday', key='type', value='text')
        setSubField(fields, 'birthday', key='value', value=lambda f: date_format(item.birthday, format='MONTH_DAY_FORMAT', use_l10n=True))

        return fields

    filter_cuteform = IDOLS_CUTEFORM

    class ItemView(MagiCollection.ItemView):

        def to_fields(self, item, order=None, extra_fields=None, exclude_fields=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None: order = []

            values = []
            for fieldName, verbose_name in models.Idol.MEASUREMENT_DETAILS:
                value = getattr(item, fieldName)
                exclude_fields.append(fieldName)
                if value:
                    values.append(mark_safe(u'<b>{}</b>: {} cm'.format(verbose_name, value)))
            if values:
                extra_fields.append(('measurements', {
                    'verbose_name': _('Measurements'),
                    'type': 'list',
                    'value': values,
                    'icon': 'measurements',
                    }))
            if item.school is not None:
                exclude_fields.append('i_year')
            if item.birthday is not None:
                exclude_fields += ['age', 'i_astrological_sign']
            exclude_fields.append('japanese_name')
            order = IDOL_ORDER + order

            fields = super(IdolCollection.ItemView, self).to_fields(item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            if item.birthday:
                if item.astrological_sign is not None:
                    setSubField(fields, 'birthday', key='icon', value=None)
                    setSubField(fields, 'birthday', key='image', value=staticImageURL(item.i_astrological_sign, folder='i_astrological_sign', extension='png'))
                if item.age:
                    setSubField(fields, 'birthday', key='type', value='text_annotation')
                    setSubField(fields, 'birthday', key='annotation', value=_('{age} years old').format(age=item.age))

            if item.school and item.year:
                    setSubField(fields, 'school', key='type', value='title_text')
                    setSubField(fields, 'school', key='title', value=item.t_school)
                    setSubField(fields, 'school', key='value', value='{}'.format(unicode(item.t_year)))

            setSubField(fields, 'description', key='type', value='long_text')

            if item.japanese_name:
                if get_language() == 'ja':
                    setSubField(fields, 'name', key='value', value=item.japanese_name)
                else:
                    setSubField(fields, 'name', key='type', value='text_annotation')
                    setSubField(fields, 'name', key='annotation', value=item.japanese_name)

            return fields

    class ListView(MagiCollection.ListView):
        filter_form = forms.IdolFilterForm
        item_template = custom_item_template
        per_line = 6
        page_size = 18
        default_ordering = '-i_school'

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        allow_delete = True

############################################################
# Events Collection

EVENT_FIELDS_PER_VERSION = ['image', 'countdown', 'start_date', 'end_date']

EVENT_ITEM_FIELDS_ORDER = [
    'banner', 'title', 'type', 'unit',
] + [
    u'{}{}'.format(_v['prefix'], _f) for _v in models.Account.VERSIONS.values()
    for _f in EVENT_FIELDS_PER_VERSION
]

EVENTS_ICONS = {
    'title': 'id',
    'jp_start_date': 'date', 'jp_end_date': 'date',
    'ww_start_date': 'date', 'ww_end_date': 'date',
    'tw_start_date': 'date', 'tw_end_date': 'date',
    'kr_start_date': 'date', 'kr_end_date': 'date',
    'cn_start_date': 'date', 'cn_end_date': 'date',
    'type': 'toggler',
}

class EventCollection(MagiCollection):
    queryset = models.Event.objects.all()
    title = _('Event')
    plural_title = _('Events')
    multipart = True
    form_class = forms.EventForm
    reportable = False
    blockable = False
    translated_fields = ('title', )
    icon = 'event'
    navbar_link_list = 'schoolidolfestival'

    _version_images = { _k: _v['image'] for _k, _v in models.Account.VERSIONS.items() }
    _version_prefixes = { _k: _v['prefix'] for _k, _v in models.Account.VERSIONS.items() }

    filter_cuteform = {
        'i_unit': {
        },
        'version': {
            'to_cuteform': lambda k, v: EventCollection._version_images[k],
            'image_folder': 'language',
            'transform': CuteFormTransform.ImagePath,
        },
    }

    def to_fields(self, view, item, *args, **kwargs):

        fields = super(EventCollection, self).to_fields(view, item, *args, icons=EVENTS_ICONS,  images={
                'unit': staticImageURL(item.i_unit, folder='i_unit', extension='png'),
        }, **kwargs)

        setSubField(fields, 'jp_start_date', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'jp_end_date', key='timezones', value=['Asia/Tokyo', 'Local time'])

        setSubField(fields, 'ww_start_date', key='timezones', value=['UTC', 'Local time'])
        setSubField(fields, 'ww_end_date', key='timezones', value=['UTC', 'Local time'])

        setSubField(fields, 'tw_start_date', key='timezones', value=['Asia/Taipei', 'Local time'])
        setSubField(fields, 'tw_end_date', key='timezones', value=['Asia/Taipei', 'Local time'])

        setSubField(fields, 'kr_start_date', key='timezones', value=['Asia/Seoul', 'Local time'])
        setSubField(fields, 'kr_end_date', key='timezones', value=['Asia/Seoul', 'Local time'])

        setSubField(fields, 'cn_start_date', key='timezones', value=['UTC', 'Local time'])
        setSubField(fields, 'cn_end_date', key='timezones', value=['UTC', 'Local time'])

        return fields

    class ItemView(MagiCollection.ItemView):

        def to_fields(self, item, order=None, extra_fields=None, exclude_fields=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None: order = []
            exclude_fields.append('c_versions')
            for version, version_details in models.Account.VERSIONS.items():
                
                #Create countdown if event is upcoming/ongoing
                status = getattr(item, u'{}status'.format(version_details['prefix']))
                if status and status != 'ended':
                    start_date = getattr(item, u'{}start_date'.format(version_details['prefix']))
                    end_date = getattr(item, u'{}end_date'.format(version_details['prefix']))
                    extra_fields += [
                        (u'{}countdown'.format(version_details['prefix']), {
                            'verbose_name': string_concat(version_details['translation'], ' - ', _('Countdown')),
                            'value': mark_safe(u'<span class="fontx1-5 countdown" data-date="{date}" data-format="{sentence}"></h4>').format(
                                date=torfc2822(end_date if status == 'current' else start_date),
                                sentence=_('{time} left') if status == 'current' else _('Starts in {time}'),
                            ),
                            'icon': 'hourglass',
                            'type': 'html',
                        }),
                    ]                        
            
            order = EVENT_ITEM_FIELDS_ORDER + order
            fields = super(EventCollection.ItemView, self).to_fields(
                item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            return fields

    class ListView(MagiCollection.ListView):
        filter_form = forms.EventFilterForm
        per_line = 2
        default_ordering = '-jp_start_date'

    def _modification_extra_context(self, context):
        if 'js_variables' not in context:
            context['js_variables'] = {}
        context['js_variables']['version_prefixes'] = jsv(self._version_prefixes)
        context['js_variables']['fields_per_version'] = jsv(EVENT_FIELDS_PER_VERSION)

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']
        ajax_callback = 'loadVersions'

        def extra_context(self, context):
            super(EventCollection.AddView, self).extra_context(context)
            self.collection._modification_extra_context(context)

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        ajax_callback = 'loadVersions'
        allow_delete = True

        def extra_context(self, context):
            super(EventCollection.EditView, self).extra_context(context)
            self.collection._modification_extra_context(context)

############################################################
# Songs Collection

SONG_FIELDS_PER_DIFFICULTY = ['notes', 'difficulty']

SONG_ICONS = {
    'title': 'song', 'romaji':' song', 'versions': 'world', 'locations': 'world',
    'unlock': 'unlock', 'daily': 'trade', 'b_side_start': 'date',
    'b_side_end': 'date', 'release': 'date', 'itunes_id': 'play',
    'length': 'times','bpm': 'hp', 'master_swipe': 'index',
    'b-side': 'times',
}

SONG_CUTEFORM = {
    'i_attribute': {
    },
    'i_unit': {
    },
    'i_subunit': {
    },
    'version': {
        'to_cuteform': lambda k, v: SongCollection._version_images[k],
        'image_folder': 'language',
        'transform': CuteFormTransform.ImagePath,
    },
    'available': {
        'type': CuteFormType.YesNo,
    },
    'location': {
        'transform': CuteFormTransform.Flaticon,
        'to_cuteform': lambda k, v: SongCollection._location_to_cuteform[k],
    },
}
subUnitMergeCuteForm(SONG_CUTEFORM)

class SongCollection(MagiCollection):
    queryset = models.Song.objects.all()
    title = _('Song')
    plural_title = _('Songs')
    multipart = True
    form_class = forms.SongForm
    reportable = False
    blockable = False
    filter_cuteform = SONG_CUTEFORM
    translated_fields = ('title', )
    icon = 'song'
    navbar_link_list = 'lovelive'

    _version_images = { _k: _v['image'] for _k, _v in models.Account.VERSIONS.items() }
    _version_prefixes = { _k: _v['prefix'] for _k, _v in models.Account.VERSIONS.items() }
    _location_to_cuteform = {
        'hits': 'deck',
        'daily': 'trade',
        'bside': 'hourglass',
    }

    def to_fields(self, view, item, *args, **kwargs):

        fields = super(SongCollection, self).to_fields(view, item, *args, icons=SONG_ICONS,  images={
                'attribute': staticImageURL(item.i_attribute, folder='i_attribute', extension='png'),
                'unit': staticImageURL(item.i_unit, folder='i_unit', extension='png'),
                'subunit': staticImageURL(item.i_subunit, folder='i_subunit', extension='png'),
        }, **kwargs)

        setSubField(fields, 'b_side_start', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'b_side_end', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'release', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'length', key='value', value=lambda f: item.length_in_minutes)
        for _difficulty, tl in models.Song.DIFFICULTIES:
            setSubField(fields, '{}_notes'.format(_difficulty), key='icon', value='combo')
            setSubField(fields, '{}_rating'.format(_difficulty), key='image', value=staticImageURL(
                getattr(item, '{}_rating'.format(_difficulty)) if 0<getattr(item, '{}_rating'.format(_difficulty))<14 else 0,
                folder='stars', extension='png'))

        return fields

    class ItemView(MagiCollection.ItemView):
        top_illustration = 'include/topSongItem'
        
        def to_fields(self, item, order=None, extra_fields=None, exclude_fields=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None: order = []              

            values = u' '
            for fieldName, verbose_name in models.Song.SONGWRITERS:
                value = getattr(item, fieldName)
                exclude_fields.append(fieldName)
                if value:
                    values+=u'<b>{}:</b> {}<br />'.format(verbose_name, value)
            if values and values is not u' ':
                extra_fields.append(('songwriters', {
                    'verbose_name': _('Songwriters'),
                    'type': 'html',
                    'value': mark_safe(u'<div class="songwriters-details">{}</div>'.format(values)),
                    'icon': 'author',
                    }))                
  
            status = getattr(item, 'status')
            if status and status != 'ended':
                start_date = getattr(item, 'b_side_start')
                end_date = getattr(item, 'b_side_end')
                extra_fields += [
                    ('b_side_countdown', {
                        'verbose_name': _('B-Side'),
                        'value': mark_safe(toCountDown(
                            date=end_date if status == 'current' else start_date,
                            sentence=_('{time} left') if status == 'current' else _('Starts in {time}'),
                            classes=['fontx1-5'],
                        )),                  
                        'icon': 'hourglass',
                        'type': 'html',
                    }),
                ]
            else:   
                exclude_fields += ['b_side_start', 'b_side_end']

            #Currently available
            extra_fields += [
                ('availability', {
                    'verbose_name': _('Currently available'),
                    'value': True if getattr(item, 'available') == True else False,
                    'icon': 'help',
                    'type': 'bool',
                }),
            ]

            #Difficulty info
            for difficulty, d_verbose in models.Song.DIFFICULTIES:
                rating = getattr(item, u'{}_rating'.format(difficulty))
                notes = getattr(item, u'{}_notes'.format(difficulty))
                if rating != None or notes != None:
                    extra_fields.append((difficulty, {
                        'verbose_name': mark_safe('<img class="song-difficulty" src="{}"'.format(
                            staticImageURL(difficulty, folder='difficulty', extension='png'))),
                        'image': staticImageURL(rating if 0<rating<14 else 0, folder='stars', extension='png'),
                        'type': 'html',
                        'value': mark_safe(generateDifficulty(rating, notes)),
                    }))
                exclude_fields.append(difficulty)
                exclude_fields.append(u'{}_rating'.format(difficulty))
                exclude_fields.append(u'{}_notes'.format(difficulty))

            exclude_fields+=['title', 'romaji', 'cover', 'i_attribute', 'i_unit', 'i_subunit',
                'c_locations', 'b_side_master', 'master_swipe']

            order = ['itunes_id', 'length', 'bpm', 'c_versions', 'availability', 'unlock',
                     'daily', 'b_side_countdown', 'b_side_start', 'b_side_end', 'easy', 'normal', 'hard', 'expert',
                     'master', 'songwriters', 'release'] + order

            fields = super(SongCollection.ItemView, self).to_fields(
                item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            if item.b_side_master is True:
                setSubField(fields, 'b_side_countdown', key='verbose_name_subtitle', value='MASTER')
            setSubField(fields, 'b_side_start', key='verbose_name', value=_('Beginning'))
            setSubField(fields, 'b_side_end', key='verbose_name', value=_('End'))

            setSubField(fields, 'unlock', key='type', value='text')
            setSubField(fields, 'unlock', key='value', value=_('Rank {}').format(item.unlock))

            if difficulty is 'master' and item.master_swipe is True:
                setSubField(fields, 'master', key='verbose_name_subtitle', value=_('with SWIPE notes'))

            return fields
        
    def _modification_extra_context(self, context):
        if 'js_variables' not in context:
            context['js_variables'] = {}
        context['js_variables']['version_prefixes'] = jsv(self._version_prefixes)
        context['js_variables']['locations_related'] = jsv(models.Song.LOCATIONS_RELATED)
        
    class ListView(MagiCollection.ListView):
        filter_form = forms.SongFilterForm
        item_template = custom_item_template
        per_line = 4
        default_ordering = '-release'
        ajax_pagination_callback = 'loadSongs'

        def extra_context(self, context):
            super(SongCollection.ListView, self).extra_context(context)
            self.collection._modification_extra_context(context)

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']
        ajax_callback = 'loadSongs'

        def extra_context(self, context):
            super(SongCollection.AddView, self).extra_context(context)
            self.collection._modification_extra_context(context)

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        ajax_callback = 'loadSongs'
        allow_delete = True

        def extra_context(self, context):
            super(SongCollection.EditView, self).extra_context(context)
            self.collection._modification_extra_context(context)

        def to_translate_form_class(self):
            super(SongCollection.EditView, self).to_translate_form_class()
            self._translate_form_class = forms.to_translate_song_form_class(self._translate_form_class)
