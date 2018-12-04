import datetime
from magi import forms
from django.core.validators import MinValueValidator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.utils import (
    PastOnlyValidator,
)
from magi.forms import AutoForm, MagiFiltersForm, MagiFilter
from sukutomo import models
from sukutomo.django_translated import t

############################################################
# Account

class AccountForm(forms.AccountForm):
    start_date = forms.forms.DateField(required=False, label=_('Start Date'), validators=[
        PastOnlyValidator,
        MinValueValidator(datetime.date(2013, 4, 16)),
    ])

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        if 'fake' in self.fields:
            del(self.fields['fake'])
        if 'transfer_code' in self.fields:
            del(self.fields['transfer_code'])
        if 'nickname' in self.fields and self.request.user.is_authenticated():
            self.fields['nickname'].initial = self.request.user.username

############################################################
############################################################
############################################################
############################################################

############################################################
# Idol

class IdolForm(AutoForm):
    class Meta:
        model = models.Idol
        save_owner_on_creation = True
        fields = '__all__'

class IdolFilterForm(MagiFiltersForm):
    merge_fields = [
        ['i_unit', 'i_subunit'],
    ]
    search_fields = ['name', 'japanese_name', 'hobbies', 'favorite_food', 'least_favorite_food', 'description']

    ordering_fields = [
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
        ('unit', _('Unit')),
        ('i_school', _('School')),
        ('birthday', _('Birthday')),
        ('age', _('Age')),
        ('height', _('Height')),
        ('bust', _('Bust')),
        ('waist', _('Waist')),
        ('hips', _('Hips')),
    ]

    def __init__(self, *args, **kwargs):
        super(IdolFilterForm, self).__init__(*args, **kwargs)
        self.reorder_fields(['search', 'i_unit_i_subunit'])

    class Meta:
        model = models.Idol
        fields = ('search', 'i_attribute', 'i_school', 'i_year', 'i_astrological_sign', 'i_blood')

############################################################
############################################################
############################################################

############################################################
# School Idol Festival (SIF)

############################################################
# Event

class SIFEventForm(AutoForm):

    jp_start_date = forms.forms.DateField(label=string_concat(_('Japanese version'), ' - ', _('Beginning')), required=False)
    jp_end_date = forms.forms.DateField(label=string_concat(_('Japanese version'), ' - ', _('End')), required=False)

    ww_start_date = forms.forms.DateField(label=string_concat(_('Worldwide version'), ' - ', _('Beginning')), required=False)
    ww_end_date = forms.forms.DateField(label=string_concat(_('Worldwide version'), ' - ', _('End')), required=False)

    tw_start_date = forms.forms.DateField(label=string_concat(_('Taiwanese version'), ' - ', _('Beginning')), required=False)
    tw_end_date = forms.forms.DateField(label=string_concat(_('Taiwanese version'), ' - ', _('End')), required=False)

    kr_start_date = forms.forms.DateField(label=string_concat(_('Korean version'), ' - ', _('Beginning')), required=False)
    kr_end_date = forms.forms.DateField(label=string_concat(_('Korean version'), ' - ', _('End')), required=False)

    cn_start_date = forms.forms.DateField(label=string_concat(_('Chinese version'), ' - ', _('Beginning')), required=False)
    cn_end_date = forms.forms.DateField(label=string_concat(_('Chinese version'), ' - ', _('End')), required=False)

    class Meta:
        model = models.SIFEvent
        save_owner_on_creation = True
        fields = '__all__'

class SIFEventFilterForm(MagiFiltersForm):
    search_fields = ['title', 'd_titles']

    ordering_fields = [
        ('jp_start_date', string_concat(_('Date'), ' (', _('Japanese version'), ')')),
        ('ww_start_date', string_concat(_('Date'), ' (', _('Worldwide version'), ')')),
        ('tw_start_date', string_concat(_('Date'), ' (', _('Taiwanese version'), ')')),
        ('kr_start_date', string_concat(_('Date'), ' (', _('Korean version'), ')')),
        ('cn_start_date', string_concat(_('Date'), ' (', _('Chinese version'), ')')),
        ('title', _('Title')),
    ]

    version = forms.forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=u'"{}"'.format(value)))

    class Meta:
        model = models.SIFEvent
        fields = ('search', 'i_type', 'i_unit', 'version')
