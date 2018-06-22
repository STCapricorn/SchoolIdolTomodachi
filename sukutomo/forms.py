import datetime
from magi import forms
from django.core.validators import MinValueValidator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.utils import PastOnlyValidator
from magi.forms import AutoForm, MagiFiltersForm, MagiFilter
from sukutomo import models
from sukutomo.django_translated import t

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

class IdolForm(AutoForm):
    class Meta:
        model = models.Idol
        save_owner_on_creation = True
        fields = '__all__'

class IdolFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'hobbies', 'favorite_food', 'least_favorite_food', 'description']

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

    class Meta:
        model = models.Idol
        fields = ('search', 'i_attribute', 'i_unit', 'i_subunit', 'i_school', 'i_year', 'i_astrological_sign', 'i_blood')

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

class SongForm(AutoForm):

    release = forms.forms.DateField(label=_('Release date'), required=False)
    b_side_start = forms.forms.DateField(label=string_concat(_('B-Side'), ' - ', _('Beginning')), required=False)
    b_side_end = forms.forms.DateField(label=string_concat(_('B-Side'), ' - ', _('End')), required=False)

    def save(self, commit=False):
        instance = super(SongForm, self).save(commit=False)
        if instance.release:
            instance.release = instance.release.replace(hour=7, minute=00)
        status = getattr(instance, 'status')
        if status is 'ended':
            instance.remove_c('locations', ['bside'])
        else:
            if instance.b_side_start:
                instance.b_side_start = instance.b_side_start.replace(hour=7, minute=00)
            if instance.b_side_end:
                instance.b_side_end = instance.b_side_end.replace(hour=7, minute=00)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Song
        save_owner_on_creation = True
        fields = '__all__'

class SongFilterForm(MagiFiltersForm):
    class Meta:
        model = models.Song
        fields = ('search', 'i_unit', 'i_subunit')
