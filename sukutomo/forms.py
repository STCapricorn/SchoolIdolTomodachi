import datetime
from magi import forms
from django.conf import settings as django_settings
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.item_model import i_choices
from magi.utils import PastOnlyValidator
from magi.forms import AutoForm, MagiFiltersForm, MagiFilter
from sukutomo import models
from sukutomo.django_translated import t
from django.utils.safestring import mark_safe

############################################################
# Form utils

SUB_UNIT_CHOICE_FIELD = forms.forms.ChoiceField(
    choices=BLANK_CHOICE_DASH + [
        (u'{}'.format(i), unit) for i, unit in i_choices(models.Idol.UNIT_CHOICES)
    ] + [
        (u'{}'.format(i + 2), subunit)
        for i, subunit in i_choices(models.Idol.SUBUNIT_CHOICES)
    ],
    label=_('Unit'),
    initial=None,
)

def sub_unit_to_queryset(prefix=''):
    def _sub_unit_to_queryset(form, queryset, request, value):
        if int(value) < 2:
            return queryset.filter(**{ u'{}i_unit'.format(prefix): value })
        elif int(value) < 10:
            return queryset.filter(**{ u'{}i_subunit'.format(prefix): int(value) - 2 })
        return queryset
    return _sub_unit_to_queryset

IDOL_SUB_UNIT_CHOICE_FIELD = forms.forms.ChoiceField(
    choices=BLANK_CHOICE_DASH + [
        (u'{}'.format(i), unit) for i, unit in i_choices(models.Song.UNIT_CHOICES)
    ] + [
        (u'{}'.format(i + 2), subunit)
        for i, subunit in i_choices(models.Song.SUBUNIT_CHOICES)
    ] + [
        (u'{}'.format(id + 10), name)
        for (id, name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])
    ],
    label=string_concat(_('Unit'), ' / ', _('Idol')),
    initial=None,
)

def idol_sub_unit_to_queryset(prefix=''):
    def _idol_sub_unit_to_queryset(form, queryset, request, value):
        if int(value) < 2:
            return queryset.filter(**{ u'{}i_unit'.format(prefix): value })
        elif int(value) < 10:
            return queryset.filter(**{ u'{}i_subunit'.format(prefix): int(value) - 2 })
        elif value:
            return queryset.filter(**{ u'idol_id': int(value) - 10})
        return queryset
    return _idol_sub_unit_to_queryset

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
# Idol

class IdolForm(AutoForm):
    def save(self, commit=False):
        instance = super(IdolForm, self).save(commit=False)
        
        # Make All Birthday Years Equal (for filter)
        if instance.birthday:
            instance.birthday = instance.birthday.replace(year=2000)
            
        if commit:
            instance.save()
        return instance
        
    class Meta:
        model = models.Idol
        save_owner_on_creation = True
        fields = '__all__'

class IdolFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'color', 'hobbies', 'favorite_food', 'least_favorite_food', 'description']

    ordering_fields = [
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
        ('i_school', _('School')),
        ('birthday', _('Birthday')),
        ('age', _('Age')),
        ('height', _('Height')),
        ('bust', _('Bust')),
        ('waist', _('Waist')),
        ('hips', _('Hips')),
    ]

    sub_unit = SUB_UNIT_CHOICE_FIELD
    sub_unit_filter = MagiFilter(to_queryset=sub_unit_to_queryset())

    class Meta:
        model = models.Idol
        fields = ('search', 'sub_unit', 'i_school', 'i_year', 'i_attribute', 'i_astrological_sign', 'i_blood')

############################################################
# Event

class EventForm(AutoForm):

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

    def save(self, commit=False):
        instance = super(EventForm, self).save(commit=False)
        
        # Set Version Date Times
        for version in models.Account.VERSIONS.keys():
            for timing in ['start', 'end']:
                field_name = u'{version}_{timing}_date'.format(version=version.lower(), timing=timing)
                date = getattr(instance, field_name, None)
                if date:
                    setattr(instance, field_name, date.replace(
                        hour=int(models.Event.TIMES_PER_VERSION[version][timing]['hour']),
                        minute=int(models.Event.TIMES_PER_VERSION[version][timing]['minute'])))
                    
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Event
        save_owner_on_creation = True
        fields = '__all__'

class EventFilterForm(MagiFiltersForm):
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
        model = models.Event
        fields = ('search', 'i_type', 'i_unit', 'version')

############################################################
# Song

class SongForm(AutoForm):

    release = forms.forms.DateField(label=_('Release date'), required=False)
    b_side_start = forms.forms.DateField(label=string_concat(_('B-Side'), ' - ', _('Beginning')), required=False)
    b_side_end = forms.forms.DateField(label=string_concat(_('B-Side'), ' - ', _('End')), required=False)

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        if 'c_versions' in self.fields:
            self.fields['c_versions'].choices = [(name, verbose) for name, verbose in self.fields['c_versions'].choices if name not in ['KR', 'TW']]

    def save(self, commit=False):
        instance = super(SongForm, self).save(commit=False)
        
        # Set Song Date Times
        for field in ['release', 'b_side_start', 'b_side_end']:
            date = getattr(instance, field, None)
            if date:
                setattr(instance, field, date.replace(
                    hour=int(models.Song.DATE_TIMES[field]['hour']),
                    minute=int(models.Song.DATE_TIMES[field]['minute'])))
                
        # Remove B-Side When Ended
        status = getattr(instance, 'status')
        if status is 'ended':
            instance.remove_c('locations', ['bside'])
            
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Song
        save_owner_on_creation = True
        fields = '__all__'

def to_translate_song_form_class(cls):
    class _TranslateSongForm(cls):
        class Meta(cls.Meta):
            fields = ['romaji'] + cls.Meta.fields
    return _TranslateSongForm

class SongFilterForm(MagiFiltersForm):
    search_fields = ['title', 'japanese_title', 'd_titles', 'romaji', 'unlock'] + dict(models.Song.SONGWRITERS).keys()

    ordering_fields = [
        ('release', _('Release date')),
        ('title', _('Title')),
        ('japanese_title', string_concat(_('Title'), ' (', _('Japanese'), ')')),
        ('romaji', string_concat(_('Title'), ' (', _('Romaji'), ')')),
        ('length', _('Length')),
        ('bpm', _('Beats per minute')),
        ('expert_rating', mark_safe(_('{} &#9734 rating').format('EXPERT'))),
        ('expert_notes', _('{} notes').format('EXPERT')),
        ('master_rating', mark_safe(_('{} &#9734 rating').format('MASTER'))),
        ('master_notes', _('{} notes').format('MASTER')),
    ]

    merge_fields = {
        'sub_unit': ['i_unit', 'i_subunit'],
    }

    location = forms.forms.ChoiceField(label=_('Location'), choices=BLANK_CHOICE_DASH + models.Song.LOCATIONS_CHOICES)
    location_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_locations__contains=value))

    version = forms.forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=value))

    def _available_to_queryset(form, queryset, request, value):
        if int(value) == 2:
            return queryset.filter(Q(b_side_start__lte=timezone.now(), b_side_end__gte=timezone.now()) | Q(release__lte=timezone.now()))
        elif int(value) == 3:
            return queryset.filter(
                Q(release=None) & (Q(b_side_start__gte=timezone.now()) | Q(b_side_end__lte=timezone.now(), release=None)) | Q(release__gte=timezone.now()) | Q(release=None)
            )
        return queryset

    available = forms.forms.NullBooleanField(initial=None, required=False, label=_('Currently available'))
    available_filter = MagiFilter(to_queryset=_available_to_queryset)

    def __init__(self, *args, **kwargs):
        super(SongFilterForm, self).__init__(*args, **kwargs)
        if 'version' in self.fields:
            self.fields['version'].choices = [(name, verbose) for name, verbose in self.fields['version'].choices if name not in ['KR', 'TW']]
        self.reorder_fields(['search', 'sub_unit', 'i_attribute', 'location', 'version', 'available'])
            
    class Meta:
        model = models.Song
        fields = ('search', 'i_attribute', 'location', 'version', 'available')
