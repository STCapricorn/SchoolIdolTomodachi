# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils.formats import dateformat
from django.utils.safestring import mark_safe
from django.utils.translation import string_concat
from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection
from magi.utils import staticImageURL, CuteFormType, CuteFormTransform, custom_item_template, torfc2822, setSubField, jsv
from sukutomo import forms, models

############################################################
# Account Collection

class AccountCollection(_AccountCollection):
    form_class = forms.AccountForm

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
    'name': 'id',
    'japanese_name': 'id',
    'school': 'max-bond',
    'year': 'scoreup',
    'age': 'scoreup',
    'birthday': 'event',
    'height': 'id',
    'blood': 'hp',
    'bust': 'id',
    'waist': 'id',
    'hips': 'id',
    'hobbies': 'star',
    'favorite_food': 'heart',
    'least_favorite_food' : 'heart-empty',
    'description': 'id',
}

IDOLS_CUTEFORM = {
    'i_unit': {
    },
    'i_subunit': {
        'image_folder': 'i_subunit',
        'title': _('Subunit'),
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
    icon = 'idolized'

    def to_fields(self, view, item, *args, **kwargs):

        fields = super(IdolCollection, self).to_fields(view, item, *args, icons=IDOLS_ICONS,  images={
                'attribute': staticImageURL(item.i_attribute, folder='i_attribute', extension='png'),
                'unit': staticImageURL(item.i_unit, folder='i_unit', extension='png'),
                'subunit': staticImageURL(item.i_subunit, folder='i_subunit', extension='png'),
                'astrological_sign': staticImageURL(item.i_astrological_sign, folder='i_astrological_sign', extension='png'),
        }, **kwargs)

        if item.japanese_name is not None and get_language() == 'ja':
            setSubField(fields, 'name', key='value', value=item.japanese_name)

        setSubField(fields, 'birthday', key='type', value='text')
        setSubField(fields, 'birthday', key='value', value=lambda f: dateformat.format(item.birthday, "F d"))

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
                    'icon': 'scoreup',
                    }))
            if item.school is not None:
                exclude_fields.append('i_year')
            if item.birthday is not None:
                exclude_fields += ['age', 'i_astrological_sign']
            exclude_fields.append('japanese_name')

            order = ['image', 'name', 'japanese_name', 'attribute', 'unit', 'subunit', 'school', 'year',
                     'astrological_sign', 'birthday', 'age', 'blood', 'measurements', 'hobbies', 'favorite_food',
                     'least_favorite_food', 'description'] + order

            fields = super(IdolCollection.ItemView, self).to_fields(item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            if item.birthday is not None:
                if item.astrological_sign is not None:
                    setSubField(fields, 'birthday', key='icon', value=None)
                    setSubField(fields, 'birthday', key='image', value=staticImageURL(item.i_astrological_sign, folder='i_astrological_sign', extension='png'))
                if item.age is not None:
                    setSubField(fields, 'birthday', key='type', value='title_text')
                    setSubField(fields, 'birthday', key='title', value=lambda f: dateformat.format(item.birthday, "F d"))
                    setSubField(fields, 'birthday', key='value', value=_('{age} years old').format(age=item.age))
                else:
                    setSubField(fields, 'birthday', key='type', value='text')
                    setSubField(fields, 'birthday', key='value', value=lambda f: dateformat.format(item.birthday, "F d"))

            if item.school is not None and item.i_year is not None:
                    setSubField(fields, 'school', key='type', value='title_text')
                    setSubField(fields, 'school', key='title', value=item.t_school)
                    setSubField(fields, 'school', key='value', value='{}'.format(unicode(item.t_year)))

            setSubField(fields, 'description', key='type', value='long_text')

            if item.japanese_name is not None:
                if get_language() == 'ja':
                    setSubField(fields, 'name', key='value', value=item.japanese_name)
                else:
                    setSubField(fields, 'name', key='type', value='title_text')
                    setSubField(fields, 'name', key='title', value=item.name)
                    setSubField(fields, 'name', key='value', value=item.japanese_name)

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

EVENT_FIELDS_PER_VERSION = ['banner', 'countdown', 'start_date', 'end_date']

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
                status = getattr(item, u'{}status'.format(version_details['prefix']))
                if status and status != 'ended':
                    start_date = getattr(item, u'{}start_date'.format(version_details['prefix']))
                    end_date = getattr(item, u'{}end_date'.format(version_details['prefix']))
                    extra_fields += [
                        (u'{}countdown'.format(version_details['prefix']), {
                            'verbose_name': string_concat(version_details['translation'], ' ',  _('version'), ' - ', _('Countdown')),
                            'value': mark_safe(u'<span class="fontx1-5 countdown" data-date="{date}" data-format="{sentence}"></h4>').format(
                                date=torfc2822(end_date if status == 'current' else start_date),
                                sentence=_('{time} left') if status == 'current' else _('Starts in {time}'),
                            ),
                            'icon': 'times',
                            'type': 'html',
                        }),
            ]
            exclude_fields.append('start_date')
            exclude_fields.append('end_date')
            order = EVENT_ITEM_FIELDS_ORDER + order
            fields = super(EventCollection.ItemView, self).to_fields(
                item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            return fields

    class ListView(MagiCollection.ListView):
        filter_form = forms.EventFilterForm
        per_line = 2
        default_ordering = 'jp_start_date'

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

SONGS_ICONS = {
    'title': 'id', 'romaji':'id', 'versions':'world', 'locations':'world',
    'unlock':'perfectlock', 'daily':'toggler', 'b_side_start': 'date',
    'b_side_end': 'date', 'release':'date', 'itunes_id':'play',
    'length':'times','bpm':'hp', 'master_swipe':'index',
    'hits': 'deck', 'daily': 'trade', 'b-side': 'times',
}

class SongCollection(MagiCollection):
    queryset = models.Song.objects.all()
    title = _('Song')
    plural_title = _('Songs')
    multipart = True
    form_class = forms.SongForm
    reportable = False
    blockable = False
    translated_fields = ('title', )
    icon = 'song'

    _version_images = { _k: _v['image'] for _k, _v in models.Account.VERSIONS.items() }
    _version_prefixes = { _k: _v['prefix'] for _k, _v in models.Account.VERSIONS.items() }
    _location_to_cuteform = {
        'hits': 'deck',
        'daily': 'trade',
        'bside': 'times',
    }

    filter_cuteform = {
        'i_attribute': {
        },
        'i_unit': {
        },
        'i_subunit': {
            'image_folder': 'i_subunit',
            'title': _('Subunit'),
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'version': {
            'to_cuteform': lambda k, v: SongCollection._version_images[k],
            'image_folder': 'language',
            'transform': CuteFormTransform.ImagePath,
        },
        'availability': {
            'type': CuteFormType.YesNo,
        },
        'location': {
            'transform': CuteFormTransform.Flaticon,
            'to_cuteform': lambda k, v: SongCollection._location_to_cuteform[k],
        },
    }

    def to_fields(self, view, item, *args, **kwargs):

        fields = super(SongCollection, self).to_fields(view, item, *args, icons=SONGS_ICONS,  images={
                'attribute': staticImageURL(item.i_attribute, folder='i_attribute', extension='png'),
                'unit': staticImageURL(item.i_unit, folder='i_unit', extension='png'),
                'subunit': staticImageURL(item.i_subunit, folder='i_subunit', extension='png'),
        }, **kwargs)

        setSubField(fields, 'b_side_start', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'b_side_end', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'release', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'length', key='value', value=lambda f: item.length_in_minutes)

        return fields

    class ItemView(MagiCollection.ItemView):
        
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
                    'icon': 'id',
                    }))                
  
            status = getattr(item, 'status')
            if status and status != 'ended':
                start_date = getattr(item, 'b_side_start')
                end_date = getattr(item, 'b_side_end')
                if item.b_side_master is True:
                    verbose = string_concat(_('B-Side'), ' - ', _('Countdown'), '  (MASTER)')
                else:
                    verbose = string_concat(_('B-Side'), ' - ', _('Countdown'))
                extra_fields += [
                    ('countdown', {
                        'verbose_name': verbose,
                        'value': mark_safe(u'<span class="fontx1-5 countdown" data-date="{date}" data-format="{sentence}"></h4>').format(
                            date=torfc2822(end_date if status == 'current' else start_date),
                            sentence=_('{time} left') if status == 'current' else _('Starts in {time}'),
                        ),
                        
                        'icon': 'times',
                        'type': 'html',
                    }),
                    ]
                  
            else:
                exclude_fields.append('b_side_start')
                exclude_fields.append('b_side_end')

            availability = getattr(item, 'available')
            if availability == 'currently available':
                av_value = True
            else:
                av_value = False
            extra_fields += [
                ('availability', {
                    'verbose_name': _('Currently available'),
                    'value': av_value,
                    'icon': 'help',
                    'type': 'bool',
                }),
            ]

            for difficulty, d_verbose in models.Song.DIFFICULTIES:
                difficulties = u' '
                difficultystar = u'{}_difficulty'.format(difficulty)
                difficultynote = u'{}_notes'.format(difficulty)
                difficultystars = getattr(item, difficultystar)
                difficultynotes = getattr(item, difficultynote)
                temps = u'{} &#9734 rating'.format(difficultystars)
                tempn = u'{} notes'.format(difficultynotes)
                if difficultystars:
                    if difficultynotes:
                        difficulties += u'{}<br />{}'.format(temps, tempn)
                        if difficulty is 'master' and item.master_swipe is True:
                            difficulties += u'<br />{}'.format(_('with SWIPE notes'))
                    else:
                        difficulties += u'{}'.format(temps)
                elif difficultynotes:
                    difficulties += u'{}'.format(tempn)
                    if difficulty is 'master' and item.master_swipe is True:
                            difficulties += u'<br />{}'.format(_('with SWIPE notes'))
                if difficulties is not u' ':
                    extra_fields.append((difficulty, {
                    'verbose_name': d_verbose,
                    'type': 'html',
                    'value': difficulties,
                    }))
                exclude_fields.append(difficulty)
                exclude_fields.append(difficultynote)
                exclude_fields.append(difficultystar)

            exclude_fields.append('romaji')
            exclude_fields.append('b_side_master')
            exclude_fields.append('c_locations')
            exclude_fields.append('master_swipe')

            order = ['cover', 'title', 'attribute', 'unit', 'subunit', 'itunes_id', 'length', 'bpm', 'c_versions', 'availability', 'unlock',
                     'daily', 'countdown', 'b_side_start', 'b_side_end', 'easy', 'normal', 'hard', 'expert',
                     'master', 'songwriters', 'release'] + order

            fields = super(SongCollection.ItemView, self).to_fields(
                item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            if item.romaji and item.romaji != item.title:
                setSubField(fields, 'title', key='type', value='title_text')
                setSubField(fields, 'title', key='title', value=item.title)
                setSubField(fields, 'title', key='value', value=item.romaji)

            setSubField(fields, 'unlock', key='type', value='text')
            setSubField(fields, 'unlock', key='value', value=u'Rank {}'.format(item.unlock))

            setSubField(fields, 'easy', key='image', value=staticImageURL('easy', folder='difficulty', extension='png'))
            setSubField(fields, 'normal', key='image', value=staticImageURL('normal', folder='difficulty', extension='png'))
            setSubField(fields, 'hard', key='image', value=staticImageURL('hard', folder='difficulty', extension='png'))
            setSubField(fields, 'expert', key='image', value=staticImageURL('expert', folder='difficulty', extension='png'))
            setSubField(fields, 'master', key='image', value=staticImageURL('master', folder='difficulty', extension='png'))

            return fields
        
    def _modification_extra_context(self, context):
        if 'js_variables' not in context:
            context['js_variables'] = {}
        context['js_variables']['version_prefixes'] = jsv(self._version_prefixes)
        
    class ListView(MagiCollection.ListView):
        filter_form = forms.SongFilterForm
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

class CardCollection(MagiCollection):
    queryset = models.Card.objects.all()
    title = _('Card')
    plural_title = _('Cards')
    multipart = True
    form_class = forms.CardForm
    reportable = False
    blockable = False
    icon = 'card'
