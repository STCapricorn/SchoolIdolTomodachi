# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.translation import string_concat
from magi.item_model import getInfoFromChoices
from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection, PrizeCollection as _PrizeCollection
from magi.utils import staticImageURL, CuteFormType, CuteFormTransform, custom_item_template, torfc2822, setSubField, jsv
from sukutomo import forms, models

############################################################
# Prize Collection

class PrizeCollection(_PrizeCollection):
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
    'image', 'name', 'japanese_name', 'attribute', 'unit', 'subunit', 'school',
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

SONGS_ICONS = {
    'title': 'id', 'romaji':'id', 'versions':'world', 'locations':'world',
    'unlock':'unlock', 'daily':'toggler', 'b_side_start': 'date',
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
    navbar_link_list = 'lovelive'

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
                        
                        'icon': 'hourglass',
                        'type': 'html',
                    }),
                    ]
                  
            else:
                exclude_fields.append('b_side_start')
                exclude_fields.append('b_side_end')

            available = getattr(item, 'available')
            if available == True:
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

            exclude_fields.append('title')
            exclude_fields.append('romaji')
            exclude_fields.append('cover')
            exclude_fields.append('i_attribute')
            exclude_fields.append('i_unit')
            exclude_fields.append('i_subunit')
            exclude_fields.append('c_locations')
            exclude_fields.append('b_side_master')
            exclude_fields.append('master_swipe')

            order = ['itunes_id', 'length', 'bpm', 'c_versions', 'availability', 'unlock',
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

############################################################
# Card Collection

CARD_AUTO_EXCLUDE = [
    'limited', 'promo', 'support', 'rate', 'i_dependency', 'chance',
    'number', 'length', 'i_center', 'i_group', 'boost_percent',
    'smile_min', 'pure_min', 'cool_min', 'hp', 'i_skill_type',
] + models.Card.IDOLIZED_FIELDS + models.Card.UNIDOLIZED_FIELDS

CARDS_CUTEFORM = {
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
    'i_rarity': {
        'image_folder': 'rarity_3',
        'title': _('Rarity'),
    },
    'version': {
        'to_cuteform': lambda k, v: EventCollection._version_images[k],
        'image_folder': 'language',
        'transform': CuteFormTransform.ImagePath,
    },
    'idol': {
        'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
    },
    'skill': {
        'transform': CuteFormTransform.FlaticonWithText, 
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'i_skill_type': {
            'transform': CuteFormTransform.Flaticon,
            'to_cuteform': lambda _k, _v: SKILL_TYPE_ICONS[models.Skill.get_reverse_i('skill_type', _k)],
        },
    'in_set': {
        'transform': CuteFormTransform.FlaticonWithText, 
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'i_group': {
        'transform': CuteFormTransform.Flaticon,
        'to_cuteform': lambda k, v: CardCollection._center_boost_to_cuteform[models.Card.get_reverse_i('group', k)]
    },
    'card_type': {
        'to_cuteform': lambda k, v: CardCollection._card_type_to_cuteform[k],
        'transform': CuteFormTransform.Flaticon,
    }
}

CARDS_ICONS = {
    'name': 'id', 'card_id': 'id', 'versions': 'world', 'release': 'date',
    'images': 'pictures', 'icons': 'pictures', 'transparents': 'pictures',
    'art': 'pictures', 'hp': 'hp', 'details': 'author',
}

CARD_IMAGES = {
    ('image', _('Images')),
    ('icon', _('Icons')),
    ('transparent', _('Transparents')),
    ('art', _('Art')),
}

CARD_ORDER = [
    'card_id', 'name', 'idol_details', 'i_rarity', 'i_attribute',
    'c_versions', 'release', 'set', 'main_skill', 'leader_skill',
    'icons', 'images', 'arts', 'transparents', 'details'
]

class CardCollection(MagiCollection):
    queryset = models.Card.objects.all()
    title = _('Card')
    plural_title = _('Cards')
    multipart = True
    form_class = forms.CardForm
    reportable = False
    blockable = False
    translated_fields = ('name', 'details')
    icon = 'deck'
    navbar_link_list = 'schoolidolfestival'

    _center_boost_to_cuteform = {
        'unit':'circles-grid',
        'subunit':'share',
        'year':'education',
    }

    _card_type_to_cuteform = {
        'perm':'chest',
        'limited':'times',
        'promo':'promo',
    }

    filter_cuteform = CARDS_CUTEFORM

    def to_fields(self, view, item, *args, **kwargs):

        # Add/Edit view auto-see All-attribute rarity symbols
        #Item/List view see proper attribute v. when known
        if item.attribute:
            rarityfolder='rarity_' + str(item.i_attribute)
        else:
            rarityfolder='rarity_3'

        fields = super(CardCollection, self).to_fields(view, item, *args, icons=CARDS_ICONS,  images={
                'attribute': staticImageURL(item.i_attribute, folder='i_attribute', extension='png'),
                'rarity': staticImageURL(item.i_rarity, folder=rarityfolder, extension='png'),
        }, **kwargs)

        setSubField(fields, 'release', key='timezones', value=['Asia/Tokyo'])
        setSubField(fields, 'card_id', key='type', value='text')
        setSubField(fields, 'card_id', key='value', value=u'#{}'.format(item.card_id))
        return fields

    class ItemView(MagiCollection.ItemView):
        top_illustration = 'items/cardItem'
        ajax_callback = 'loadCard'
        
        def to_fields(self, item, order=None, extra_fields=None, exclude_fields=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None: order = []

            #Add Idol field
            if item.idol:
                extra_fields.append(('idol_details', {
                    'verbose_name': _('Idol'),
                    'type': 'html',
                    'value': string_concat('<a href="', item.idol.item_url, '"data-ajax-url="', item.idol.ajax_item_url,
                        '"data-ajax-title="', item.idol, '">', item.idol.t_name, '<img class="idol-small-image" src="',
                            item.idol.image_url,'"></img></a>'),
                    'icon': 'idol',
                }))

            #Add skill                
            if item.skill:
                # Get list of variables to parse through
                SKILL_REPLACE = models.Card.SKILL_REPLACE
                if item.idol:
                    SKILL_REPLACE += models.Card.IDOL_REPLACE
                skill_details = getattr(item, 'skill_details')

                #Either insert the variable info or ???
                for variable in SKILL_REPLACE:
                    if variable in models.Card.IDOL_REPLACE:
                        _item = item.idol
                    else:
                        _item = item
                    og = skill_details
                    if getattr(_item, variable, None) is not None:
                        #If translatable, get translated val instead
                        if variable in models.Card.SKILL_REPLACE_TRANSLATE:
                            var = getattr(_item, 't_{}'.format(variable))
                        else:
                            var = getattr(_item, variable)
                    else:
                        var = '???'
                    var_re = '{' + variable + '}'
                    skill_details = og.replace(var_re, mark_safe(var))

                #creates skill field 
                skill_sentence=_('{} (Level 1)').format(skill_details)  
                extra_fields.append(('main_skill', {
                    'verbose_name': _('Skill'),
                    'type': 'html',
                    'value': skill_sentence,
                    'icon': 'sparkle',
                }))

            #Add center skill
            if item.center:
                leader_skill = getattr(item, 'center_details')
                leader_skill = leader_skill.format(getattr(item, 't_attribute'))  
                if item.rarity in ['UR', 'SSR']:
                    leader_second = _('plus {group} members\' {} pts. up by {}%')
                    if item.group is not 0 and item.boost_percent is not None:
                        for gvariable, ggvariable in models.Card.GROUP_CHOICES:
                            if ggvariable is item.t_group:
                                if item.t_group is not _('Unit'):
                                    og = leader_second
                                    var = getattr(item.idol, 't_' + gvariable)
                                    leader_second = og.replace('{group}', var)
                                else:
                                    og = leader_second
                                    leader_second = og.replace('{group}', item.idol.unit)
                        leader_second = leader_second.format(item.t_attribute, item.boost_percent)
                extra_fields.append(('leader_skill', {
                    'verbose_name': _('Leader Skill'),
                    'type': 'text',
                    'value': leader_skill,
                    'icon': 'center',
                }))

            #Add set
            if item.in_set:
                extra_fields.append(('set', {
                    'verbose_name': _('Set'),
                    'type': 'link',
                    'ajax_link': item.in_set.ajax_cards_url,
                    'link': item.in_set.cards_url,
                    'link_text': unicode(item.in_set),
                    'icon': 'scout-box',
                }))

            #Add images
            for image, verbose_name in CARD_IMAGES:
                #Regular images for each type
                CARD_IMAGE_TYPES = [
                    getattr(item, u'{}_url'.format(image)),
                    getattr(item, u'{}_idol_url'.format(image)),
                ]
                exclude_fields.append(image)
                exclude_fields.append(image + '_idol')
                #Old images
                if image is not 'transparent':
                    CARD_IMAGE_TYPES += [
                        getattr(item, u'old_{}_url'.format(image)),
                        getattr(item, u'old_{}_idol_url'.format(image))
                    ]
                    exclude_fields.append('old_' + image)
                    exclude_fields.append('old_' + image + '_idol')

                #if type of image, append specific image field  
                if getattr(item, image):
                    extra_fields.append((u'{}s'.format(image), {
                        'verbose_name': verbose_name,
                        'type': 'images_links',
                        'images': [{
                            'value': image_url.format(image),
                            'link': image_url.format(image),
                            'verbose_name': verbose_name,
                            'link_text': verbose_name,
                        } for image_url in CARD_IMAGE_TYPES if image_url],
                        'icon': 'pictures',
                    }))

            # Exclude certain fields by default
            for field in CARD_AUTO_EXCLUDE:
                exclude_fields.append(field)

            order = CARD_ORDER + order
            
            fields = super(CardCollection.ItemView, self).to_fields(
                item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            if item.skill:
                setSubField(fields, 'main_skill', key='value', value=string_concat(
                    item.skill.card_html(), '<br />', skill_sentence))

            if item.center:
                setSubField(fields, 'leader_skill', key='type', value='title_text')
                setSubField(fields, 'leader_skill', key='title', value=string_concat(item.t_attribute, ' ', item.t_center))
                # if info for 2nd half of center skill is available
                if item.group is not 0 and item.boost_percent is not None:
                    setSubField(fields, 'leader_skill', key='value', value=string_concat(leader_skill, ', ', leader_second))

            return fields
        
    class ListView(MagiCollection.ListView):
        filter_form = forms.CardFilterForm
        item_template = custom_item_template
        per_line = 3
        default_ordering = '-release,-card_id'
        ajax_pagination_callback = 'loadCardList'

        def get_queryset(self, queryset, parameters, request):
            queryset = super(CardCollection.ListView, self).get_queryset(queryset, parameters, request)
            if request.GET.get('ordering', None) in ['max_smile', 'max_pure, max_cool']:
                queryset = queryset.extra(select={
                    'max_smile': 'smile_max_idol' or 'smile_max' or 'smile_min',
                    'max_pure': 'pure_max_idol' or 'pure_max' or 'pure_min',
                    'max_cool': 'cool_max_idol' or 'cool_max' or 'cool_min',
                })
            return queryset

        def ordering_fields(self, item, only_fields=None, *args, **kwargs):
            fields = super(CardCollection.ListView, self).ordering_fields(item, *args, only_fields=only_fields, **kwargs)
            if 'max_smile' in only_fields:
                fields['max_smile'] = {
                    'verbose_name':  _('Smile'),
                    'value': item.smile_max_idol or item.smile_max or item.smile_min or '???',
                    'type': 'text',
                    'image': staticImageURL('0', folder='i_attribute', extension='png'),
                }
            if 'max_pure' in only_fields:
                fields['max_pure'] = {
                    'verbose_name':  _('Pure'),
                    'value': item.pure_max_idol or item.pure_max or item.pure_min or '???',
                    'type': 'text',
                    'image': staticImageURL('1', folder='i_attribute', extension='png'),
                }
            if 'max_cool' in only_fields:
                fields['max_cool'] = {
                    'verbose_name':  _('Cool'),
                    'value': item.cool_max_idol or item.cool_max or item.cool_min or '???',
                    'type': 'text',
                    'image': staticImageURL('2', folder='i_attribute', extension='png'),
                }

            return fields

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']
        ajax_callback = 'loadCardForm'

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        allow_delete = True
        ajax_callback = 'loadCardForm'

############################################################
# Skill Collection

SKILL_TYPE_ICONS = {
    'score':'scoreup', 'pl':'perfectlock',
    'heal':'healer', 'stat':'statistics',
    'support':'megaphone',
}

class SkillCollection(MagiCollection):
    queryset = models.Skill.objects.all()
    title = _('Skill')
    plural_title = _('Skills')
    multipart = True
    form_class = forms.SkillForm
    reportable = False
    blockable = False
    translated_fields = ('name', 'details',)
    icon = 'sparkle'
    navbar_link = False
    permissions_required = ['manage_main_items']

    filter_cuteform = {
        'i_skill_type': {
            'transform': CuteFormTransform.Flaticon,
            'to_cuteform': lambda _k, _v: SKILL_TYPE_ICONS[models.Skill.get_reverse_i('skill_type', _k)],
        },
    }
    
    def to_fields(self, view, item, *args, **kwargs):
    
        fields = super(SkillCollection, self).to_fields(view, item, *args,
            icons={'name':'id', 'skill_type':'category', 'details':'author'}, **kwargs)

        return fields

    class ListView(MagiCollection.ListView):
        filter_form = forms.SkillFilterForm
        item_template = custom_item_template
        per_line = 6

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        allow_delete = True

############################################################
# Set Collection

class SetCollection(MagiCollection):
    queryset = models.Set.objects.all()
    title = _('Set')
    plural_title = _('Sets')
    multipart = True
    form_class = forms.SetForm
    reportable = False
    blockable = False
    translated_fields = ('title', )
    icon = 'scout-box'
    navbar_link_list = 'schoolidolfestival'

    _set_type_icons = { 'gacha':'scout-box', 'event':'event' }

    filter_cuteform = {
        'i_unit': {
        },
        'i_set_type': {
            'transform': CuteFormTransform.Flaticon,
            'to_cuteform': lambda k, v: SetCollection._set_type_icons[models.Set.get_reverse_i('set_type', k)],
        },
    }

    class ListView(MagiCollection.ListView):
        filter_form = forms.SetFilterForm
        item_template = custom_item_template
        per_line = 4

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        allow_delete = True
