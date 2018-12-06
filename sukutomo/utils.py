import random
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from magi.utils import mergedFieldCuteForm, staticImageURL

def generateDifficulty(rating, notes):
    string = _('{} &#9734 rating').format(rating) if rating != None else ''
    string += '<br />' if string != '' else ''
    string += _('{} notes').format(notes) if notes != None else ''
    return string

def subUnitMergeCuteForm(cuteform):
    mergedFieldCuteForm(cuteform, {
        'title': _('Unit'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    }, OrderedDict ([
        ('i_unit', lambda k, v: staticImageURL(k, folder='i_unit', extension='png')),
        ('i_subunit', lambda k, v: staticImageURL(k, folder='i_subunit', extension='png')),
    ]), merged_field_name='sub_unit')


