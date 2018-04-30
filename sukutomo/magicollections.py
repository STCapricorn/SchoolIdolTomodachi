# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils.formats import dateformat
from django.utils.safestring import mark_safe
from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection
from magi.utils import staticImageURL, CuteFormType, CuteFormTransform, custom_item_template
from magi.utils import setSubField
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
            'to_cuteform': lambda k, v: models.Account.VERSIONS[models.Account.get_reverse_i('version', k)]['icon'],
            'transform': CuteFormTransform.FlaticonWithText,
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
