import datetime
from magi import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.utils import PastOnlyValidator
from magi.forms import AutoForm, MagiFiltersForm
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

            
